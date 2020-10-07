# coding=gbk
import asyncio
import difflib
import json
import random
import time
import traceback
from datetime import datetime

import aiohttp

from source.config.configPraser import configPraser

from source.data.bean.Commits import Commits
from source.data.bean.Diff import Diff
from source.data.bean.MergeRequest import MergeRequest
from source.data.bean.Notes import Notes
from source.data.bean.Position import Position
from source.data.service.AsyncSqlHelper import AsyncSqlHelper
from source.data.service.GraphqlHelper import GraphqlHelper
from source.data.service.ProxyHelper import ProxyHelper
from source.data.service.TextCompareUtils import TextCompareUtils
from source.utils.Logger import Logger
from source.utils.StringKeyUtils import StringKeyUtils


class AsyncApiHelper:
    """ʹ��aiohttp�첽ͨѶ"""

    owner = None
    repo = None
    repo_id = None

    @staticmethod
    def setRepo(owner, repo):  # ʹ��֮ǰ������Ŀ����������
        AsyncApiHelper.owner = owner
        AsyncApiHelper.repo = repo

    @staticmethod
    def setRepoId(repo_id):  # GitLab��Ҫ��ʹ��ǰ������Ŀ��id
        AsyncApiHelper.repo_id = repo_id

    @staticmethod
    def getAuthorizationHeaders(header):
        """����Github ��Token������֤"""
        if header is not None and isinstance(header, dict):
            if configPraser.getAuthorizationToken():
                header[StringKeyUtils.STR_HEADER_AUTHORIZAITON] = (StringKeyUtils.STR_HEADER_TOKEN
                                                                   + configPraser.getAuthorizationToken())
        return header

    @staticmethod
    def getPrivateTokensHeaders(header):
        """����Gitlab ��Token������֤"""
        if header is not None and isinstance(header, dict):
            if configPraser.getAuthorizationToken():
                header[StringKeyUtils.STR_HEADER_PRIVATE_TOKEN] = (configPraser.getPrivateToken())
        return header

    @staticmethod
    def getUserAgentHeaders(header):
        """������ԣ� ��������agent"""
        if header is not None and isinstance(header, dict):
            # header[self.STR_HEADER_USER_AGENT] = self.STR_HEADER_USER_AGENT_SET
            header[StringKeyUtils.STR_HEADER_USER_AGENT] = random.choice(StringKeyUtils.USER_AGENTS)
        return header

    @staticmethod
    def getMediaTypeHeaders(header):
        if header is not None and isinstance(header, dict):
            header[StringKeyUtils.STR_HEADER_ACCEPT] = StringKeyUtils.STR_HEADER_MEDIA_TYPE
        return header

    @staticmethod
    async def getProxy():
        """��ȡ����ip���е�ip  ��ϸ�� ProxyHelper"""
        if configPraser.getProxy():
            proxy = await ProxyHelper.getAsyncSingleProxy()
            if configPraser.getPrintMode():
                print(proxy)
            if proxy is not None:
                return StringKeyUtils.STR_PROXY_HTTP_FORMAT.format(proxy)
        return None

    @staticmethod
    async def parserMergeRequest(resultJson):
        try:
            res = None
            if configPraser.getApiVersion() == StringKeyUtils.API_VERSION_RESET:
                if not AsyncApiHelper.judgeNotFind(resultJson):
                    res = MergeRequest.parser.parser(resultJson)
            elif configPraser.getApiVersion() == StringKeyUtils.API_VERSION_GRAPHQL:
                pass
                # GraphQL�ӿڽ������ܻ᲻��һ��
            if res is not None:
                res.repository = AsyncApiHelper.owner + '/' + AsyncApiHelper.repo
                return res
        except Exception as e:
            print(e)

    @staticmethod
    async def parserNotes(resultJson):
        try:
            resList = []
            if configPraser.getApiVersion() == StringKeyUtils.API_VERSION_RESET:
                if not AsyncApiHelper.judgeNotFind(resultJson):
                    if resultJson is not None and isinstance(resultJson, list):
                        for notesData in resultJson:
                            notes = Notes.parser.parser(notesData)
                            if notes is not None:
                                resList.append(notes)
            elif configPraser.getApiVersion() == StringKeyUtils.API_VERSION_GRAPHQL:
                pass
                # GraphQL�ӿڽ������ܻ᲻��һ��
            return resList
        except Exception as e:
            print(e)

    @staticmethod
    async def parserCommit(resultJson):
        try:
            resList = []
            if configPraser.getApiVersion() == StringKeyUtils.API_VERSION_RESET:
                if not AsyncApiHelper.judgeNotFind(resultJson):
                    if resultJson is not None and isinstance(resultJson, list):
                        for commitData in resultJson:
                            commit = Commits.parser.parser(commitData)
                            if commit is not None:
                                resList.append(commit)
            elif configPraser.getApiVersion() == StringKeyUtils.API_VERSION_GRAPHQL:
                pass
                # GraphQL�ӿڽ������ܻ᲻��һ��
            return resList
        except Exception as e:
            print(e)

    @staticmethod
    def judgeNotFind(resultJson):
        if resultJson is not None and isinstance(json, dict):
            if resultJson.get(StringKeyUtils.STR_KEY_MESSAGE) == StringKeyUtils.STR_NOT_FIND:
                return True
            if resultJson.get(StringKeyUtils.STR_KEY_MESSAGE) == StringKeyUtils.STR_FAILED_FETCH:
                return True
        return False

    @staticmethod
    def judgeNotFindV4(resultJson):
        """v4 �ӿڵ�not find�жϺ�v3�Ĳ�����ͬ"""
        if resultJson is not None and isinstance(json, dict):
            if resultJson.get(StringKeyUtils.STR_KEY_ERRORS) is not None:
                return True
        return False

    @staticmethod
    async def judgeChangeTrigger(session, pr_author, change_sha, notes):
        position = notes.position
        if position is not None and isinstance(position, Position):
            head_sha = position.head_sha
            username = notes.author_user_name
            if username == pr_author:
                notes.change_trigger = -2  # -2 ���������Լ�����
                return
            diffs = await AsyncApiHelper.getDiffBetweenCommits(session, head_sha, change_sha)
            if diffs is not None and isinstance(diffs, list):
                for diffData in diffs:
                    diff = Diff.parser.parser(diffData)
                    if diff is not None:
                        if diff.new_path == notes.position.new_path or diff.old_path == notes.position.old_path:
                            print(diff.diff)
                            """����diff hunk"""
                            TextCompareUtils.patchParser(diff.diff)


    @staticmethod
    def urlAppendParams(url, paramsDict):
        isFirst = True
        for k, v in paramsDict.items():
            if isFirst:
                url += f'?{k}={v}'
                isFirst = False
            else:
                url += f'&{k}={v}'
        return url

    @staticmethod
    async def getDiffBetweenCommits(session, sha1, sha2):
        api = AsyncApiHelper.getCommitCompareApi()
        api = AsyncApiHelper.urlAppendParams(api, {'from': sha1, 'to': sha2})
        json = await AsyncApiHelper.fetchBeanData(session, api)
        if json is not None and isinstance(json, dict):
            return json.get(StringKeyUtils.STR_KEY_DIFFS, None)

    @staticmethod
    async def downloadInformation(merge_request_iid, semaphore, mysql, statistic):
        """��ȡһ����Ŀ ����merge-request ��ص���Ϣ"""

        """����issue  ��Ҫ��дdownloadInformation���� 
           ֻ��pull-request�Ļ�ȡת��Ϊissue
        """
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                try:
                    beanList = []  # �����ռ���Ҫ�洢��bean��
                    """�Ȼ�ȡpull request��Ϣ"""
                    api = AsyncApiHelper.getMergeRequestApi(merge_request_iid)
                    json = await AsyncApiHelper.fetchBeanData(session, api)
                    print(json)
                    merge_request = await AsyncApiHelper.parserMergeRequest(json)
                    print(merge_request)
                    usefulMergeRequestsCount = 0

                    if merge_request is not None:
                        usefulMergeRequestsCount = 1
                        """��Ҫ�䱣�����ݿ�Ķ������beanList����"""
                        beanList.append(merge_request)

                        if merge_request.diff_refs is not None:
                            beanList.append(merge_request.diff_refs)
                        if merge_request.author is not None:
                            beanList.append(merge_request.author)
                        if merge_request.merged_by_user is not None:
                            beanList.append(merge_request.merged_by_user)
                        if merge_request.closed_by_user is not None:
                            beanList.append(merge_request.closed_by_user)

                        pr_author = merge_request.author_user_name

                        """��ȡcommits"""
                        api = AsyncApiHelper.getCommitApi(merge_request_iid)
                        json = await AsyncApiHelper.fetchBeanData(session, api)
                        print(json)
                        commitList = []
                        if json is not None and isinstance(json, list):
                            commitList = await AsyncApiHelper.parserCommit(json)

                        """��ȡnotes"""
                        api = AsyncApiHelper.getNotesApi(merge_request_iid)
                        json = await AsyncApiHelper.fetchBeanData(session, api)
                        print(json)

                        """��ȡ��һ��commit��sha"""
                        change_sha = commitList[0].id

                        nodesList = []
                        if json is not None and isinstance(json, list):
                            nodesList = await AsyncApiHelper.parserNotes(json)

                        # """��������"""
                        # for nodes in nodesList:
                        #     if nodes.position is not None:
                        #         await AsyncApiHelper.judgeChangeTrigger(session, pr_author, change_sha, nodes)

                        print(beanList)

                    """���ݿ�洢"""
                    await AsyncSqlHelper.storeBeanDateList(beanList, mysql)

                    # ����ͬ������
                    statistic.lock.acquire()
                    statistic.usefulRequestNumber += usefulMergeRequestsCount
                    """������������ͬ��������ͳ��"""

                    print("useful pull request:", statistic.usefulRequestNumber,
                          " useful review:", statistic.usefulReviewNumber,
                          " useful review comment:", statistic.usefulReviewCommentNumber,
                          " useful issue comment:", statistic.usefulIssueCommentNumber,
                          " useful commit:", statistic.usefulCommitNumber,
                          " cost time:", datetime.now() - statistic.startTime)
                    statistic.lock.release()
                except Exception as e:
                    print(e)

    @staticmethod
    def getGraphQLApi():
        api = StringKeyUtils.API_GITHUB + StringKeyUtils.API_GRAPHQL
        return api

    @staticmethod
    def getMergeRequestApi(merge_request_iid):
        api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_GITLAB_MERGE_PULL_REQUEST
        api = api.replace(StringKeyUtils.STR_GITLAB_REPO_ID, str(AsyncApiHelper.repo_id))
        api = api.replace(StringKeyUtils.STR_GITLAB_MR_NUMBER, str(merge_request_iid))
        return api

    @staticmethod
    def getCommitCompareApi():
        api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_GITLAB_COMMITS_COMPARE
        api = api.replace(StringKeyUtils.STR_GITLAB_REPO_ID, str(AsyncApiHelper.repo_id))
        return api

    @staticmethod
    def getNotesApi(merge_request_iid):
        api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_GITLAB_NOTES
        api = api.replace(StringKeyUtils.STR_GITLAB_REPO_ID, str(AsyncApiHelper.repo_id))
        api = api.replace(StringKeyUtils.STR_GITLAB_MR_NUMBER, str(merge_request_iid))
        return api

    @staticmethod
    def getCommitApi(merge_request_iid):
        api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_GITLAB_COMMITS
        api = api.replace(StringKeyUtils.STR_GITLAB_REPO_ID, str(AsyncApiHelper.repo_id))
        api = api.replace(StringKeyUtils.STR_GITLAB_MR_NUMBER, str(merge_request_iid))
        return api

    @staticmethod
    async def fetchBeanData(session, api, isMediaType=False):
        """�첽��ȡ����ͨ�ýӿڣ���Ҫ��"""

        """��ʼ������ͷ"""
        headers = {}
        headers = AsyncApiHelper.getUserAgentHeaders(headers)
        headers = AsyncApiHelper.getPrivateTokensHeaders(headers)  # ������token�����е����� ��ע�͵� 2020.10.7

        while True:
            """�Ե�������ѭ���ж� ֱ������ɹ����ߴ���"""

            """��ȡ����ip  ip��ȡ��Ҫ���д����"""
            proxy = await AsyncApiHelper.getProxy()
            if configPraser.getProxy() and proxy is None:  # �Դ����û��ip�����������
                print('no proxy and sleep!')
                await asyncio.sleep(20)
            else:
                break

        try:
            async with session.get(api, ssl=False, proxy=proxy
                    , headers=headers, timeout=configPraser.getTimeout()) as response:
                print("rate:", response.headers.get(StringKeyUtils.STR_HEADER_RATE_LIMIT_REMIAN))
                print("status:", response.status)
                if response.status == 403:
                    await ProxyHelper.judgeProxy(proxy.split('//')[1], ProxyHelper.INT_KILL_POINT)
                    raise 403
                elif proxy is not None:
                    await ProxyHelper.judgeProxy(proxy.split('//')[1], ProxyHelper.INT_POSITIVE_POINT)
                return await response.json()
        except Exception as e:
            """�� 403�������������  ѭ������"""
            print(e)
            if proxy is not None:
                proxy = proxy.split('//')[1]
                await ProxyHelper.judgeProxy(proxy, ProxyHelper.INT_NEGATIVE_POINT)
            # print("judge end")
            """ѭ������"""
            return await AsyncApiHelper.fetchBeanData(session, api, isMediaType=isMediaType)

    @staticmethod
    async def postGraphqlData(session, api, query=None, args=None):
        """ͨ�� github graphhql�ӿ� ͨ��post����"""
        headers = {}
        headers = AsyncApiHelper.getUserAgentHeaders(headers)
        headers = AsyncApiHelper.getAuthorizationHeaders(headers)

        body = {}
        body = GraphqlHelper.getGraphlQuery(body, query)
        body = GraphqlHelper.getGraphqlVariables(body, args)
        bodyJson = json.dumps(body)
        # print("bodyjson:", bodyJson)

        while True:
            proxy = await AsyncApiHelper.getProxy()
            if configPraser.getProxy() and proxy is None:  # �Դ����û��ip�����������
                print('no proxy and sleep!')
                await asyncio.sleep(20)
            else:
                break

        try:
            async with session.post(api, ssl=False, proxy=proxy,
                                    headers=headers, timeout=configPraser.getTimeout(),
                                    data=bodyJson) as response:
                print("rate:", response.headers.get(StringKeyUtils.STR_HEADER_RATE_LIMIT_REMIAN))
                print("status:", response.status)
                if response.status == 403:
                    await ProxyHelper.judgeProxy(proxy.split('//')[1], ProxyHelper.INT_KILL_POINT)
                    raise 403
                elif proxy is not None:
                    await ProxyHelper.judgeProxy(proxy.split('//')[1], ProxyHelper.INT_POSITIVE_POINT)
                return await response.json()
        except Exception as e:
            print(e)
            if proxy is not None:
                proxy = proxy.split('//')[1]
                await ProxyHelper.judgeProxy(proxy, ProxyHelper.INT_NEGATIVE_POINT)
            print("judge end")
            return await AsyncApiHelper.postGraphqlData(session, api, query, args)

# coding=gbk

class SqlUtils:
    """���ڴ洢��SQL���"""

    STR_SQL_CREATE_TABLE = 'create table %s'

    '''Ԥ�ƴ洢�ı�����'''
    STR_TABLE_NAME_USER = 'userList'
    STR_TABLE_NAME_MERGE_REQUEST = 'mergeRequest'
    STR_TABLE_NAME_DIFF_REFS = 'diffRefs'

    '''�洢�ı��е�����'''
    STR_KEY_INT = 'int'
    STR_KEY_VARCHAR_MAX = 'varchar(8000)'
    STR_KEY_VARCHAR_MIDDLE = 'varchar(5000)'
    STR_KEY_DATE_TIME = 'datatime'
    STR_KEY_TEXT = 'text'

    '''�������'''
    STR_SQL_INSERT_TABLE_UTILS = 'insert into {0} values{1}'

    '''��ѯ����'''
    STR_SQL_QUERY_TABLE_UTILS = 'select * from {0} {1}'

    '''ɾ������'''
    STR_SQL_DELETE_TABLE_UTILS = 'delete from {0} {1}'

    '''�޸Ĳ���'''
    STR_SQL_UPDATE_TABLE_UTILS = 'update {0} {1} {2}'

    '''��ѯ���ݿ���û��ƥ���commit'''
    STR_SQL_QUERY_UNMATCH_COMMITS = 'select distinct review.repo_full_name, review.commit_id from review ' + \
                                    'where  review.commit_id not in  (select sha from gitCommit) LIMIT 2000'

    '''��ѯ���ݿ���û��ƥ�� gitfile ��commit'''
    STR_SQL_QUERY_UNMATCH_COMMIT_FILE = """select distinct commitPRRelation.repo_full_name, gitCommit.sha
                                        from gitCommit, commitPRRelation
                                        where gitCommit.sha not in (select gitFile.commit_sha from gitFile)
                                        and gitCommit.sha = commitPRRelation.sha LIMIT 2000"""

    '''��ѯ���ݿ���û��ƥ�� gitfile ��commit ͨ�� has_file_fetched�ж�'''
    STR_SQL_QUERY_UNMATCH_COMMIT_FILE_BY_HAS_FETCHED_FILE = """select distinct commitPRRelation.repo_full_name, gitCommit.sha
                                        from gitCommit, commitPRRelation
                                        where gitCommit.has_file_fetched = False
                                        and gitCommit.sha = commitPRRelation.sha LIMIT %s, 2000"""
    '''��ѯ���ݿ���û��ƥ�� gitfile ��commit ����ͨ�� has_file_fetched�ж�'''
    STR_SQL_QUERY_UNMATCH_COMMIT_FILE_COUNT_BY_HAS_FETCHED_FILE = """select count(distinct gitCommit.sha)
                                        from gitCommit, commitPRRelation
                                        where gitCommit.has_file_fetched = False
                                        and gitCommit.sha = commitPRRelation.sha"""

    '''��ѯ���ݿ���û��original_lineֵ��review comment һ��2000��'''
    STR_SQL_QUERY_NO_ORIGINAL_LINE_REVIEW_COMMENT = """select id
                                        from reviewComment
                                        where pull_request_review_id in (
                                            select id
                                            from review
                                            where repo_full_name = %s
                                              and pull_number
                                                in (select number
                                                    from pullRequest
                                                    where pullRequest.repo_full_name = %s
                                                      and pullRequest.state = 'closed' and number between %s and %s
                                                    ) 
                                        )  and original_line is null LIMIT 2000"""

    '''��ѯ���ݿ���û��original_lineֵ��review comment һ��2000��'''
    STR_SQL_QUERY_NO_ORIGINAL_LINE_REVIEW_COMMENT_COUNT = """select count(id)
                                        from reviewComment
                                        where pull_request_review_id in (
                                            select id
                                            from review
                                            where repo_full_name = %s
                                              and pull_number
                                                in (select number
                                                    from pullRequest
                                                    where pullRequest.repo_full_name = %s
                                                      and pullRequest.state = 'closed' and number between %s and %s
                                                    ) 
                                        )  and original_line is null"""

    STR_SQL_QUERY_PR_FOR_TIME_LINE = """select distinct node_id 
                                        from pullRequest 
                                        where state = 'closed' and repo_full_name = %s
                                        """


    @staticmethod
    def getInsertTableFormatString(tableName, items):

        '''��ȡ�������ı�ĸ�ʽ'''

        res = tableName
        if items.__len__() > 0:
            res += '('
            pos = 0
            for item in items:
                if (pos == 0):
                    res += item
                else:
                    res += ','
                    res += item
                pos += 1
            res += ')'
        return res

    @staticmethod
    def getInsertTableValuesString(number):
        """��ȡ�������ֵ�ĸ�ʽ"""

        res = '('
        pos = 0
        while pos < number:
            if pos == 0:
                res += '%s'
            else:
                res += ','
                res += '%s'
            pos += 1
        res += ')'
        return res

    @staticmethod
    def getQueryTableConditionString(items):

        """��ȡ��ѯ���ı�׼��ʽ"""
        res = ''
        pos = 0
        if items is not None and items.__len__() > 0:
            res += 'where'
            for item in items:
                if pos == 0:
                    res += ' '
                    res += item
                    res += '=%s'
                else:
                    res += ' and '
                    res += item
                    res += '=%s'
                pos += 1
        return res

    @staticmethod
    def getUpdateTableSetString(items):

        """��ȡ���±�����ı�׼��ʽ"""
        res = ''
        pos = 0
        if items is not None and items.__len__() > 0:
            res += 'set'
            for item in items:
                if pos == 0:
                    res += ' '
                    res += item
                    res += '=%s'
                else:
                    res += ','
                    res += item
                    res += '=%s'
                pos += 1
        return res

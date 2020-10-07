# coding=gbk
import os


class projectConfig:
    projectName = 'NJU_HUAWEI'
    PATH_CONFIG = 'source' + os.sep + 'config' + os.sep + 'config.txt'
    PATH_TEST_INPUT_EXCEL = 'data' + os.sep + 'Test200.xlsx'
    PATH_TEST_OUTPUT_EXCEL = 'data' + os.sep + 'output.xlsx'
    PATH_TEST_OUTPUT_PATH = 'data'
    PATH_STOP_WORD_HGD = 'data' + os.sep + 'HGDStopWord.txt'
    PATH_SPLIT_WORD_EXCEL = 'data' + os.sep + 'output_splitword.xlsx'
    PATH_USER_DICT_PATH = 'data' + os.sep + 'user_dict.utf8'
    PATH_TEST_CRF_INPUT = 'data' + os.sep + 'people-daily.txt'
    PATH_TEST_CRF_TEST_RESULT = 'data' + os.sep + 'test.rst'
    PATH_TEST_REVIEW_COMMENT = 'data' + os.sep + 'reviewComments.tsv'
    PATH_TEST_WINE_RED = 'data' + os.sep + 'winequality-red.xlsx'
    PATH_TEST_REVHELPER_DATA = 'data' + os.sep + 'revhelperDemoData.csv'
    PATH_TEST_FPS_DATA = 'data' + os.sep + 'FPSDemoData.tsv'
    PATH_STOP_WORD_ENGLISH = 'data' + os.sep + 'stop-words_english_1_en.txt'
    PATH_RUBY_KEY_WORD = 'data' + os.sep + 'rubyKeyWord.txt'
    PATH_CHANGE_TRIGGER = 'data' + os.sep + 'pullrequest_rails.tsv'
    PATH_COMMIT_RELATION = 'data' + os.sep + 'train' + os.sep + 'prCommitRelation'
    PATH_ISSUE_COMMENT_PATH = 'data' + os.sep + 'train' + os.sep + 'issueCommentData'
    PATH_DATA_TRAIN = 'data' + os.sep + 'train'
    PATH_COMMIT_FILE = 'data' + os.sep + 'train' + os.sep + 'commitFileData'
    PATH_SEAA = 'data' + os.sep + 'SEAA'
    PATH_PULL_REQUEST = 'data' + os.sep + 'train' + os.sep + 'pullRequestData'
    PATH_PR_CHANGE_FILE = 'data' + os.sep + 'train' + os.sep + 'prChangeFile'
    PATH_REVIEW = 'data' + os.sep + 'train' + os.sep + 'reviewData'
    PATH_TIMELINE = 'data' + os.sep + 'train' + os.sep + 'prTimeLineData'
    PATH_REVIEW_COMMENT = 'data' + os.sep + 'train' + os.sep + 'reviewCommentData'
    PATH_REVIEW_CHANGE = 'data' + os.sep + 'train' + os.sep + 'reviewChangeData'
    PATH_PULL_REQUEST_DISTANCE = 'data' + os.sep + 'train' + os.sep + 'prDistance'
    PATH_USER_FOLLOW_RELATION = 'data' + os.sep + 'train' + os.sep + 'userFollowRelation'
    PATH_USER_WATCH_REPO_RELATION = 'data' + os.sep + 'train' + os.sep + 'userWatchRepoRelation'
    PATH_STOP_WORD_STEM = 'data' + os.sep + 'stemStopWord.txt'
    PATH_COMMENT_KEY_WORD = 'data' + os.sep + 'train' + os.sep + 'commentKeyWord'

    PATH_FPS_DATA = 'data' + os.sep + 'train' + os.sep + 'FPS'
    PATH_ML_DATA = 'data' + os.sep + 'train' + os.sep + 'ML'
    PATH_IR_DATA = 'data' + os.sep + 'train' + os.sep + 'IR'
    PATH_CA_DATA = 'data' + os.sep + 'train' + os.sep + 'CA'
    PATH_PB_DATA = 'data' + os.sep + 'train' + os.sep + 'PB'
    PATH_TC_DATA = 'data' + os.sep + 'train' + os.sep + 'TC'
    PATH_CN_DATA = 'data' + os.sep + 'train' + os.sep + 'CN'
    PATH_GA_DATA = 'data' + os.sep + 'train' + os.sep + 'GA'
    PATH_CF_DATA = 'data' + os.sep + 'train' + os.sep + 'CF'
    PATH_HG_DATA = 'data' + os.sep + 'train' + os.sep + 'HG'
    PATH_AC_DATA = 'data' + os.sep + 'train' + os.sep + 'AC'
    PATH_CN_IR_DATA = 'data' + os.sep + 'train' + os.sep + 'CN_IR'
    PATH_CHREV_DATA = 'data' + os.sep + 'train' + os.sep + 'CHREV'
    PATH_XF_DATA = 'data' + os.sep + 'train' + os.sep + 'XF'
    PATH_SVM_C_DATA = 'data' + os.sep + 'train' + os.sep + 'SVM_C'
    PATH_FPS_AC_DATA = 'data' + os.sep + 'train' + os.sep + 'FPS_AC'
    PATH_IR_AC_DATA = 'data' + os.sep + 'train' + os.sep + 'IR_AC'
    PATH_CN_AC_DATA = 'data' + os.sep + 'train' + os.sep + 'CN_AC'
    PATH_RF_A_DATA = 'data' + os.sep + 'train' + os.sep + 'RF_A'
    PATH_EAREC_DATA = 'data' + os.sep + 'train' + os.sep + 'EAREC'

    PATH_CDR_DATA = 'data' + os.sep + 'train' + os.sep + 'CDR'
    PATH_ALGORITHM = 'source' + os.sep + 'scikit' + os.sep

    TEST_OUT_PUT_SHEET_NAME = 'sheet1'

    @staticmethod
    def getRootPath():
        curPath = os.path.abspath(os.path.dirname(__file__))
        projectName = projectConfig.projectName
        rootPath = os.path.join(curPath.split(projectName)[0], projectName)  # ��ȡmyProject��Ҳ������Ŀ�ĸ�·��
        return rootPath

    @staticmethod
    def getConfigPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_CONFIG)

    @staticmethod
    def getDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_TEST_OUTPUT_PATH)

    @staticmethod
    def getTestInputExcelPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_TEST_INPUT_EXCEL)

    @staticmethod
    def getTestoutputExcelPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_TEST_OUTPUT_EXCEL)

    @staticmethod
    def getStopWordHGDPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_STOP_WORD_HGD)

    @staticmethod
    def getSplitWordExcelPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_SPLIT_WORD_EXCEL)

    @staticmethod
    def getUserDictPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_USER_DICT_PATH)

    @staticmethod
    def getCRFInputData():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_TEST_CRF_INPUT)

    @staticmethod
    def getCRFTestDataResult():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_TEST_CRF_TEST_RESULT)

    @staticmethod
    def getReviewCommentTestData():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_TEST_REVIEW_COMMENT)

    @staticmethod
    def getRandomForestTestData():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_TEST_REVHELPER_DATA)

    @staticmethod
    def getFPSTestData():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_TEST_FPS_DATA)

    @staticmethod
    def getStopWordEnglishPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_STOP_WORD_ENGLISH)

    @staticmethod
    def getRubyKeyWordPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_RUBY_KEY_WORD)

    @staticmethod
    def getChangeTriggerPRPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_CHANGE_TRIGGER)

    @staticmethod
    def getPrCommitRelationPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_COMMIT_RELATION)

    @staticmethod
    def getIssueCommentPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_ISSUE_COMMENT_PATH)

    @staticmethod
    def getDataTrainPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_DATA_TRAIN)

    @staticmethod
    def getCommitFilePath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_COMMIT_FILE)

    @staticmethod
    def getReviewChangeDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_REVIEW_CHANGE)

    @staticmethod
    def getPullRequestPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_PULL_REQUEST)

    @staticmethod
    def getPullRequestDistancePath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_PULL_REQUEST_DISTANCE)

    @staticmethod
    def getFPSDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_FPS_DATA)

    @staticmethod
    def getMLDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_ML_DATA)

    @staticmethod
    def getCDRDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_CDR_DATA)

    @staticmethod
    def getIRDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_IR_DATA)

    @staticmethod
    def getACDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_AC_DATA)

    @staticmethod
    def getRF_ADataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_RF_A_DATA)

    @staticmethod
    def getPBDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_PB_DATA)

    @staticmethod
    def getGADataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_GA_DATA)

    @staticmethod
    def getTCDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_TC_DATA)

    @staticmethod
    def getCHREVDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_CHREV_DATA)

    @staticmethod
    def getCADataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_CA_DATA)

    @staticmethod
    def getSVM_CDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_SVM_C_DATA)

    @staticmethod
    def getFPS_ACDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_FPS_AC_DATA)

    @staticmethod
    def getIR_ACDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_IR_AC_DATA)

    @staticmethod
    def getCN_ACDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_FPS_AC_DATA)

    @staticmethod
    def getCNDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_CN_DATA)

    @staticmethod
    def getCN_IRDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_CN_IR_DATA)

    @staticmethod
    def getCFDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_CF_DATA)

    @staticmethod
    def getHGDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_HG_DATA)

    @staticmethod
    def getXFDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_XF_DATA)

    @staticmethod
    def getSEAADataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_SEAA)

    @staticmethod
    def getPRChangeFilePath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_PR_CHANGE_FILE)

    @staticmethod
    def getReviewDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_REVIEW)

    @staticmethod
    def getPRTimeLineDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_TIMELINE)

    @staticmethod
    def getReviewCommentDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_REVIEW_COMMENT)

    @staticmethod
    def getLogPath():
        return projectConfig.getRootPath() + os.sep + 'log'

    @staticmethod
    def getUserFollowRelation():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_USER_FOLLOW_RELATION)

    @staticmethod
    def getUserWatchRepoRelation():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_USER_WATCH_REPO_RELATION)

    @staticmethod
    def getAlgorithmPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_ALGORITHM)

    @staticmethod
    def getEARECDataPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_EAREC_DATA)

    @staticmethod
    def getStopWordStemPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_STOP_WORD_STEM)

    @staticmethod
    def getCommentKeyWordPath():
        return os.path.join(projectConfig.getRootPath(), projectConfig.PATH_COMMENT_KEY_WORD)


if __name__ == "__main__":
    print(projectConfig.getRootPath())
    print(projectConfig.getConfigPath())
    print(projectConfig.getTestInputExcelPath())
    print(projectConfig.getDataPath())
    print(projectConfig.getTestoutputExcelPath())

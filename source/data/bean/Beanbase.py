# coding=gbk

class BeanBase:
    """����������Ļ���"""

    @staticmethod
    def getItemKeyList():
        pass

    '''�ṩ�������������б�'''

    @staticmethod
    def getItemKeyListWithType():
        pass

    '''�ṩ���������ֺ�����Ԫ���б�'''

    def getValueDict(self):
        pass

    '''�ṩ�������������ֵ�'''

    @staticmethod
    def getIdentifyKeys():
        pass

    '''�ṩ�������Ψһ��ʶ'''

    '''���������漰������'''
    DATA_TYPE_INT = 0
    DATA_TYPE_DATE_TIME = 1
    DATA_TYPE_STRING = 2
    DATA_TYPE_TEXT = 3
    DATA_TYPE_BOOLEAN = 4
    DATA_TYPE_LONG_TEXT = 5

    class parser:
        '''���ڽ���json��������'''

        @staticmethod
        def parser(src):
            pass

        '''����json ����������'''

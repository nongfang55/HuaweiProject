# coding=gbk
import pymssql
from source.config.configPraser import configPraser


class DataBaseOpenHelper:
    '''�����������ݿ�ӿ���'''

    @staticmethod
    def connect():
        conn = pymssql.connect(configPraser.getDataBaseHost(),
                               configPraser.getDataBaseUserName(),
                               configPraser.getDataBasePassword())
        if conn:
            if configPraser.getPrintMode():
                print('���ݿ����ӳɹ���host:', configPraser.getDataBaseHost(), ' user:', configPraser.getDataBaseUserName())
        return conn


if __name__ == '__main__':
    conn = DataBaseOpenHelper.connect()

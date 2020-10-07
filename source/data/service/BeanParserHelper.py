# coding=gbk
from source.config.configPraser import configPraser
from source.data.bean.Beanbase import BeanBase


class BeanParserHelper:
    """bean ���һЩ����parser��ʽ"""

    @staticmethod
    def getBeansFromTuple(beanClass, columns, dataTuple):
        result = []
        if configPraser.getPrintMode():
            print(columns)
        if isinstance(beanClass, BeanBase):
            for i in dataTuple:
                """���÷������ʵ��������"""
                obj = beanClass.__class__()
                itemList = obj.getItemKeyList()
                for item in itemList:
                    value = BeanParserHelper.findItemInArray(item, columns, i)
                    if value is not None:
                        setattr(obj, item, value)
                result.append(obj)
            if configPraser.getPrintMode():
                print(result.__len__())
        return result

    @staticmethod
    def findItemInArray(item, columns, array):
        index = -1
        try:
            index = columns.index(item)
        except Exception as e:
            pass
        if index == -1:
            return None
        return array[index]


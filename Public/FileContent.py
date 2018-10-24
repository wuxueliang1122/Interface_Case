# coding=utf-8

import json
import os
from Public.GlobalVar import GlobalVar


class FileContent:
    """
    读取文件，并转换成后续要用的对应格式
    """
    def __init__(self, filename):
        self.filename = filename
        self._global_dic = GlobalVar.global_dic

    def get_json_contents(self):
        """
        :return: 读取json文件，直接将读取到的字符串转换为字典格式
        """
        # 存储文档所有数据，并将每一行数据当做数组一个元素
        try:
            with open(self.filename, 'r', encoding='utf-8', errors='ignore') as fp_object:
                self._global_dic = json.load(fp_object)
            # return self._global_dic
        except FileNotFoundError:
            print("The file" + self.filename + " is not exist.")

    def get_description(self):
        if len(self._global_dic) == 0:
            self.get_json_contents()
        print("description: ", self._global_dic['description'])
        try:
            return self._global_dic['description']
        except:
            raise ValueError("description is not exist.")

    def get_instruction(self, serial):
        """
        :return:
        """
        try:
            return self.get_caselist()[serial]['instruction']
        except:
            raise ValueError("instruction is not exist.")

    def get_api(self):
        """

        :return:
        """
        if len(self._global_dic) == 0:
            self.get_json_contents()
        # print("api:", self._global_dic['api'])
        return self._global_dic['api']

    def get_apiname(self):
        if len(self._global_dic) == 0:
            self.get_json_contents()
        # print("apiname:", self._global_dic['apiname'])
        try:
            return self._global_dic['apiname']
        except:
            raise ValueError("apiname is is not exist.")

    def get_caselist(self):
        """
        :return: 返回apiname
        """
        if len(self._global_dic) == 0:
            self.get_json_contents()
        try:
            return self._global_dic['caseList']
        except:
            raise ValueError("caseList is not exist.")

    def get_reqparams(self, serial):
        """
        :return:返回Json文档请求参数reqParams的值
        """
        if len(self._global_dic) == 0:
            self.get_json_contents()
        try:
            return self.get_caselist()[serial]["reqParams"]
        except:
            raise ValueError("reqParams is not exist.")

    def get_expectresult(self, serial):
        """    
        :param serial:
        :return:返回expectResult内容
        """
        if len(self._global_dic) == 0:
            self.get_json_contents()
        try:
            return self.get_caselist()[serial]["expectResult"]
        except:
            raise ValueError("expectResult is not exist.")

    def get_data(self, serial):
        """  
        :param serial: 
        :return: 返回expectResult中data
        """
        try:
            return self.get_expectresult(serial)['data']
        except:
            raise ValueError("data is not exist.")

    def get_datalist(self, serial):
        """
        :param serial: 
        :return: 返回data字段中dataList的值
        """
        try:
            return self.get_data(serial)['dataList']
        except:
            raise ValueError("dataList is not exist.")

    """
    def get_casenumber(self):
        if len(self._global_dic) == 0:
            self.get_json_contents()
        return len(self.get_caselist())
    """

    def get_sqldata(self, serial):
        """
        :param serial:
        :return:返回Json文档中的sql语言集
        """
        try:
            return self.get_caselist()[serial]['sql']
        except:
            raise ValueError("sql_data is not exist.")


if __name__ == '__main__':
    filename = os.path.abspath("/Users/wuxueliang/Documents/OpenSource/cheguo_auto"
                               "/Document/Wechat_Applet/brokerGetCarSourceDetail.json")
    filename1 = os.path.abspath("../Document/Wechat_Applet/brokerGetCarSourceDetail.json")
    A = FileContent(filename1)
    A.get_description()
    A.get_apiname()

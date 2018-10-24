# coding=utf-8

import requests
import unittest
import operator
from Public.FileContent import FileContent
from Public.Request import Request
from Public.Verify import Verify
from Public.SqlOperation import SqlOperation


class GetSearchLogList(unittest.TestCase):
    def setUp(self):
        self.filename = Request().dirname() + "/Document/Wechat_Applet/getSearchLogList.json"

        self.filecontent = FileContent(self.filename)
        self.apiname = self.filecontent.get_apiname()  # 获取apiname用于获得url
        self.api = self.filecontent.get_api()  # 获取api用于校验
        self.caselist = self.filecontent.get_caselist()  # 获取caselist列表，包括"reqParams"和"expectResult"

        self.verify = Verify()
        # self.result = GlobalVar().global_dic
        self.verificationErrors = []

    def get_response(self, serial):
        """

        :param serial:
        :return: 获取接口返回
        """
        url = Request().get_url(serial=serial, filename=self.filename, apiname=self.apiname)
        session = requests.session()
        response = session.post(url, timeout=1)
        if response.status_code == 200:
            return response
        else:
            raise ConnectionRefusedError("request is refused.")

    def verify_data_sql(self, serial, result):
        """
        data:从数据库取query_value值用于校验
        :param serial
        :param result
        :return: 
        """
        select_sql = self.filecontent.get_sqldata(serial)['select']
        select_result = SqlOperation().select_data_all(select_sql)
        verify_data = []
        if select_result is None:
            self.assertIsNone(result['data'], msg="result data is not NULL.")
        else:
            for data in select_result:
                verify_data.append(data[0])
            self.assertEqual(sorted(verify_data), sorted(result['data']))

    def test_get_success(self):
        """
        获取车源搜索记录
        校验点：1、message:返回值 查询搜索记录成功
               2、data:从数据库取query_value值用于校验
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {1: "获取车源搜索记录"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key - 1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

            """
            sql_data = self.filecontent.get_sqldata(serial=key - 1)
            if SqlOperation().select_data_all(sql_data['select']) is None:
                SqlOperation().update_data(sql_data['update'])
            """

            response = self.get_response(serial=key - 1)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key - 1)

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)
            print("code verify is success.")

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)
            print("message verify is success.")

            self.verify_data_sql(serial=key - 1, result=json_result)

            print("ALL END!!")

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

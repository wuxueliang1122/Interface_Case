# coding=utf-8

import requests
import unittest
import operator
from Public.FileContent import FileContent
from Public.Request import Request
from Public.Verify import Verify
from Public.SqlOperation import SqlOperation


class SaveBrokerUserFormId(unittest.TestCase):
    def setUp(self):
        self.filename = Request().dirname() + "/Document/Wechat_Applet/saveBrokerUserFormId.json"

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

    def verify_formid_sql(self, serial):
        """
        校验请求后数据库是否有生成对应的formId记录
        :return: 
        """
        select_sql = self.filecontent.get_sqldata(serial)['select']
        self.assertEqual(SqlOperation().select_data(select_sql)[0], self.filecontent.get_reqparams(serial)['formId'],
                         msg="check sql db is Error.")

    def test_get_success(self):
        """
        小程序表单提交--保存form_id
        校验点：1、message:返回值 success
               2、请求后与数据库生成的记录做对比，form_id与请求参数的form_id保持一致
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {1: "form_id保存成功"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key - 1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

            sql_data = self.filecontent.get_sqldata(serial=key - 1)
            if SqlOperation().select_data(sql_data['select']) is not None:
                SqlOperation().delete_data(sql_data['delete'])

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

            self.verify_formid_sql(serial=key - 1)

            print("ALL END!!")

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

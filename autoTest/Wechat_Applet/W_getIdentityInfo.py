# coding=utf-8

import requests
import unittest
import operator
from Public.FileContent import FileContent
from Public.Request import Request
from Public.Verify import Verify
from Public.SqlOperation import SqlOperation


class GetIdentityInfo(unittest.TestCase):
    def setUp(self):
        self.filename = Request().dirname() + "/Document/Wechat_Applet/getIdentityInfo.json"

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

    def verify_auth_status(self, serial, result):
        """
        校验auth_status=0
        :return: 
        """
        expect = self.filecontent.get_data(serial)["authStatus"]
        result = result["data"]["authStatus"]
        self.assertEqual(expect, result,
                         msg="The expect authStatus: {}, the result authStatus: {}".format(expect, result))

    def test_status_unauthorized(self):
        """
        未认证状态
        校验点：1、从数据库获取对应userid的auth_status=0
               2、message:返回值 获取认证信息成功
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {1: "未认证状态"}
        for key, value in casenum.items():
            # print(value, self.filecontent.get_instruction(serial=key-1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

            sql_data = self.filecontent.get_sqldata(serial=key - 1)
            if SqlOperation().select_data(sql_data['select']) is None:
                SqlOperation().insert_data(sql_data['insert'])

            response = self.get_response(serial=key - 1)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key - 1)

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)

            print("data verify is beginning...")
            self.verify.verify_data(expectresult=expectresult, result=json_result)

            print("authStatus verify is begining...")
            self.verify_auth_status(serial=key - 1, result=json_result)

            print("ALL END!!")

    def test_status_success(self):
        """
        认证成功状态
        校验点：1、从数据库获取对应userid的auth_status=1
               2、message:返回值 获取认证信息成功
               3、data返回的内容
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {2: "认证成功状态"}
        for key, value in casenum.items():
            # print(value, self.filecontent.get_instruction(serial=key-1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

            sql_data = self.filecontent.get_sqldata(serial=key - 1)
            if SqlOperation().select_data(sql_data['select']) is None:
                SqlOperation().insert_data(sql_data['insert'])

            response = self.get_response(serial=key - 1)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key - 1)

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)

            print("data verify is beginning...")
            self.verify.verify_data(expectresult=expectresult, result=json_result)

            print("authStatus verify is begining...")
            self.verify_auth_status(serial=key - 1, result=json_result)

            print("ALL END!!")

    def test_status_fail(self):
        """
        认证失败状态
        校验点：1、从数据库获取对应userid的auth_status=2
               2、message:返回值 获取认证信息成功
               3、data返回的内容
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {3: "认证失败状态"}
        for key, value in casenum.items():
            # print(value, self.filecontent.get_instruction(serial=key-1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

            sql_data = self.filecontent.get_sqldata(serial=key - 1)
            if SqlOperation().select_data(sql_data['select']) is None:
                SqlOperation().insert_data(sql_data['insert'])

            response = self.get_response(serial=key - 1)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key - 1)

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)

            print("data verify is beginning...")
            self.verify.verify_data(expectresult=expectresult, result=json_result)

            print("authStatus verify is begining...")
            self.verify_auth_status(serial=key - 1, result=json_result)

            print("ALL END!!")

    def test_status_ing(self):
        """
        认证中状态
        校验点：1、从数据库获取对应userid的auth_status=3
               2、message:返回值 获取认证信息成功
               3、data返回的内容
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {4: "认证中状态"}
        for key, value in casenum.items():
            # print(value, self.filecontent.get_instruction(serial=key-1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

            sql_data = self.filecontent.get_sqldata(serial=key - 1)
            if SqlOperation().select_data(sql_data['select']) is None:
                SqlOperation().insert_data(sql_data['insert'])

            response = self.get_response(serial=key - 1)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key - 1)

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)

            print("data verify is beginning...")
            self.verify.verify_data(expectresult=expectresult, result=json_result)

            print("authStatus verify is begining...")
            self.verify_auth_status(serial=key - 1, result=json_result)

            print("ALL END!!")

    def tearDown(self):
        SqlOperation().close()


if __name__ == '__main__':
    unittest.main()

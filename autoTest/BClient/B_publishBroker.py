# coding=utf-8
import unittest
import requests
import operator
from Public.FileContent import FileContent
from Public.Request import Request
from Public.Verify import Verify


class MyTestCase(unittest.TestCase):
    def setUp(self):

        self.filename = Request().dirname() + "/Document/B_Client/publishBroker.json"

        self.filecontent = FileContent(self.filename)
        self.apiname = self.filecontent.get_apiname()  # 获取apiname用于获得url
        self.api = self.filecontent.get_api()  # 获取api用于校验
        self.caselist = self.filecontent.get_caselist()  # 获取caselist列表，包括"reqParams"和"expectResult"
        # self.casenumber = self.filecontent.get_casenumber()       # 获取case数量

        self.verify = Verify()
        self.verificationErrors = []

    def get_response(self, serial):
        """

            :param serial:
            :return: 获取接口返回
            """
        url = Request().get_url(serial=serial, filename=self.filename, apiname=self.apiname)
        session = requests.session()
        response = session.post(url)
        return response

    def test_publish_success(self):
        """
        经纪人带客车源发布成功
        校验点：1、data=成功
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {1: "发布成功"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key - 1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

            response = self.get_response(serial=key - 1)
            self.verify.verify_code_200(response=response)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key - 1)

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)

            self.verify.verify_data(expectresult=expectresult, result=json_result)
            print("ALL END!!")

    def test_modify_commission(self):
        """
        经纪人带客车源修改佣金成功
        校验点：1、data=成功
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {2: "修改佣金成功"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key - 1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

            response = self.get_response(serial=key - 1)
            self.verify.verify_code_200(response=response)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key - 1)

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)

            self.verify.verify_data(expectresult=expectresult, result=json_result)
            print("ALL END!!")

    def test_cancel_publish(self):
        """
        经纪人带客车源取消发布成功
        校验点：1、data=成功
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {3: "取消发布成功"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key - 1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

            response = self.get_response(serial=key - 1)
            self.verify.verify_code_200(response=response)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key - 1)

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)

            self.verify.verify_data(expectresult=expectresult, result=json_result)
            print("ALL END!!")

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

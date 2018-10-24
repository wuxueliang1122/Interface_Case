# coding=utf-8

import requests
import unittest
import operator
from Public.FileContent import FileContent
from Public.Request import Request
from Public.Verify import Verify


class UpdateQuote(unittest.TestCase):

    def setUp(self):
        self.filename = Request().dirname() + "/Document/Public_Api/updateQuote.json"

        self.filecontent = FileContent(self.filename)
        self.apiname = self.filecontent.get_apiname()
        self.caselist = self.filecontent.get_caselist()
        self.verify = Verify()

    def get_response(self, serial):
        url = Request().get_url(serial=serial, filename=self.filename, apiname=self.apiname)
        session = requests.session()
        response = session.post(url)
        return response

    def test_updatequote_success(self):
        """
        重新报价成功
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {1: "重新报价成功，不修改报价详情"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key-1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key-1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key-1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

            response = self.get_response(serial=key-1)
            self.verify.verify_code_200(response=response)
            print(response.content)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key-1)

            print("api verify is beginning...")
            self.verify.verify_api(expectresult=expectresult, result=json_result)
            print("api verify is success.")

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)
            print("code verify is success.")

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)
            print("message verify is success.")

            print("ALL END!!")

    def test_change_commission(self):
        """
        重新报价成功，修改佣金金额
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {2: "重新报价成功，修改佣金金额"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key-1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key-1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key-1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

            response = self.get_response(serial=key-1)
            self.verify.verify_code_200(response=response)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key-1)

            print("api verify is beginning...")
            self.verify.verify_api(expectresult=expectresult, result=json_result)
            print("api verify is success.")

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)
            print("code verify is success.")

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)
            print("message verify is success.")

            print("ALL END!!")

    def test_modify_inf(self):
        """
        重新报价成功，修改其他信息,如期望售价、车辆所在地、报价有效期等
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {3: "重新报价成功，修改其他信息"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key-1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key-1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key-1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

            response = self.get_response(serial=key-1)
            self.verify.verify_code_200(response=response)
            print(response.content)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key-1)

            print("api verify is beginning...")
            self.verify.verify_api(expectresult=expectresult, result=json_result)
            print("api verify is success.")

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)
            print("code verify is success.")

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)
            print("message verify is success.")

            print("ALL END!!")

if __name__ == '__main__':
    unittest.main()

# coding=utf-8

import requests
import unittest
import operator
from Public.FileContent import FileContent
from Public.Request import Request
from Public.Verify import Verify
from Public.SqlOperation import SqlOperation


class BindCard(unittest.TestCase):
    def setUp(self):
        self.filename = Request().dirname() + "/Document/Wechat_Applet/bindCard.json"

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

    def verify_reason(self, serial, result):
        """
        校验data里面的reason字段
        :param serial: key-1
        :param result: response.json()
        :return: 
        """
        ex_reason = self.filecontent.get_expectresult(serial=serial)['data']['reason']
        r_reason = result['data']['reason']
        self.assertEqual(ex_reason, r_reason, msg="TestCase {}: {} reason verify is Fail."
                         .format(serial+1, self.filecontent.get_instruction(serial-1)))

    def verify_success(self, serial, result):
        """
        校验data里面的success字段
        :param serial: 
        :param result: 
        :return: 
        """
        ex_success = self.filecontent.get_expectresult(serial=serial)['data']['success']
        r_success = result['data']['success']
        self.assertEqual(ex_success, r_success, msg="TestCase {}: {} reason verify is Fail."
                         .format(serial + 1, self.filecontent.get_instruction(serial - 1)))

    def test_four_elem_cert_false(self):
        """
        四要素认证不通过：绑定银行卡,四要素不一致，绑卡失败
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {1: "四要素认证不通过：绑定银行卡,四要素不一致，绑卡失败"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key-1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key-1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key-1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key-1))

            response = self.get_response(serial=key-1)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key-1)
            self.verify.verify_code_200(response=response)

            print("api verify is beginning...")
            self.verify.verify_api(expectresult=expectresult, result=json_result)
            print("api verify is success.")

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)
            print("code verify is success.")

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)
            print("message verify is success.")

            print("data verify is beginning...")
            self.verify.verify_data(expectresult=expectresult, result=json_result)
            print("data verify is success.")

            print("reason verify is begining...")
            self.verify_reason(serial=key-1, result=json_result)
            print("reason verify is success.")

            print("success verify is begining...")
            self.verify_reason(serial=key - 1, result=json_result)
            print("success verify is success.")

            print("data verify is beginning...")
            self.verify.verify_data(expectresult=expectresult, result=json_result)
            print("data verify is success.")

            print("ALL END!!")

    def test_cert_success(self):
        """
        绑卡成功:前提条件-我的银行卡没有银行卡，四要素认证成功
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {2: "绑卡成功:前提条件-我的银行卡没有银行卡，四要素认证成功"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key - 1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("TestCase {}'s instruction is not Equal to CaseNum.".format(key - 1))

            sql_data = self.filecontent.get_sqldata(serial=key-1)
            if len(SqlOperation().select_data(sql_data['select'])) == 1:
                SqlOperation().delete_data(sql_data['delete'])

            response = self.get_response(serial=key - 1)
            json_result = response.json()
            print("response content: ", json_result)

            expectresult = self.filecontent.get_expectresult(serial=key - 1)
            self.verify.verify_code_200(response=response)

            print("api verify is beginning...")
            self.verify.verify_api(expectresult=expectresult, result=json_result)
            print("api verify is success.")

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)
            print("code verify is success.")

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)
            print("message verify is success.")

            print("data verify is beginning...")
            self.verify.verify_data(expectresult=expectresult, result=json_result)
            print("data verify is success.")

            print("reason verify is begining...")
            self.verify_reason(serial=key - 1, result=json_result)
            print("reason verify is success.")

            print("success verify is begining...")
            self.verify_reason(serial=key - 1, result=json_result)
            print("success verify is success.")

            print("ALL END!!")

    def test_repeat_card(self):
        """
        重复绑卡：前提条件-我的银行卡列表已经绑定了银行卡
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {3: "重复绑卡：前提条件-我的银行卡列表已经绑定了银行卡"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key - 1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("TestCase {}'s instruction is not Equal to CaseNum.".format(key - 1))

            response = self.get_response(serial=key - 1)
            json_result = response.json()
            print("response content: ", json_result)

            expectresult = self.filecontent.get_expectresult(serial=key - 1)
            self.verify.verify_code_200(response=response)

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

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

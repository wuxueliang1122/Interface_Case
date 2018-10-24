# coding=utf-8

import unittest
import requests
import operator
import time
from Public.FileContent import FileContent
from Public.Request import Request
from Public.Verify import Verify
from Public.SqlOperation import SqlOperation


class GetQuoteDetail(unittest.TestCase):

    def setUp(self):
        self.filename = Request().dirname() + "/Document/B_Client/getQuoteDetail.json"

        self.filecontent = FileContent(filename=self.filename)
        self.apiname = self.filecontent.get_apiname()
        self.caselist = self.filecontent.get_caselist()

        self.verify = Verify()
        # self.casenumber = self.filecontent.get_casenumber()

    def get_response(self, serial):
        url = Request().get_url(serial=serial, filename=self.filename, apiname=self.apiname)
        response = requests.post(url=url)
        if response.status_code == 200:
            return response
        else:
            raise ConnectionRefusedError()

    def verify_status(self, serial, result):
        """
        校验返回结果的status == auto.company_quote.status
        :param result
        :return: 
        """
        expect_status = self.filecontent.get_expectresult(serial)['status']
        result_status = result['data']['status']
        self.assertEqual(expect_status, result_status, msg="expect_status != result_status.")

    def test_offering(self):
        """
        报价中状态查询成功
        校验点：1、message:返回值 查询成功
               2、data不为空
               3、status=1
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {1: "报价中状态查询成功"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key - 1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

            # 更新数据库auto.company_search_car的search_status、is_valid和auto.company_quote的status、is_valid状态
            sql = self.filecontent.get_sqldata(serial=key - 1)
            for sql_update in sql['update']:
                SqlOperation().update_data(sql_update)

            response = self.get_response(serial=key - 1)
            self.verify.verify_code_200(response=response)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key - 1)

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)

            self.verify.verify_data_isNotNull(result=json_result)
            self.verify_status(serial=key - 1, result=json_result)

            print("ALL END!!")

    def test_offer_expired(self):
        """
        报价已过期状态查询成功
        校验点：1、message:返回值 查询成功
               2、data不为空
               3、status=2
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {2: "报价已过期状态查询成功"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key - 1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

            # 更新数据库auto.company_search_car的search_status、is_valid和auto.company_quote的status、is_valid状态
            sql = self.filecontent.get_sqldata(serial=key - 1)
            for sql_update in sql['update']:
                SqlOperation().update_data(sql_update)

            response = self.get_response(serial=key - 1)
            self.verify.verify_code_200(response=response)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key - 1)

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)

            self.verify.verify_data_isNotNull(result=json_result)
            self.verify_status(serial=key-1, result=json_result)

            print("ALL END!!")

    def test_offer_withdraw(self):
        """
        报价已撤回状态查询成功
        校验点：1、message:返回值 查询成功
               2、data不为空
               3、status=3
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {3: "报价已撤回状态查询成功"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key - 1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

            # 更新数据库auto.company_search_car的search_status、is_valid和auto.company_quote的status、is_valid状态
            sql = self.filecontent.get_sqldata(serial=key - 1)
            for sql_update in sql['update']:
                SqlOperation().update_data(sql_update)

            response = self.get_response(serial=key - 1)
            self.verify.verify_code_200(response=response)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key - 1)

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)

            self.verify.verify_data_isNotNull(result=json_result)
            self.verify_status(serial=key-1, result=json_result)

            print("ALL END!!")

    def test_offer_failure(self):
        """
        报价已失效   状态查询成功
        校验点：1、message:返回值 查询成功
               2、data不为空
               3、status=4
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {4: "报价已失效状态查询成功"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key - 1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

            # 更新数据库auto.company_search_car的search_status、is_valid和auto.company_quote的status、is_valid状态
            sql = self.filecontent.get_sqldata(serial=key - 1)
            for sql_update in sql['update']:
                SqlOperation().update_data(sql_update)

            response = self.get_response(serial=key - 1)
            self.verify.verify_code_200(response=response)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key - 1)

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)

            self.verify.verify_data_isNotNull(result=json_result)
            self.verify_status(serial=key-1, result=json_result)

            print("ALL END!!")

    def tearDown(self):
        SqlOperation().close()


if __name__ == '__main__':
    unittest.main()

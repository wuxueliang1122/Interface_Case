# coding=utf-8

import requests
import unittest
import operator
import time
from Public.FileContent import FileContent
from Public.Request import Request
from Public.Verify import Verify
from Public.SqlOperation import SqlOperation


class ConfirmBrokerOrder(unittest.TestCase):
    def setUp(self):
        self.filename = Request().dirname() + "/Document/Wechat_Applet/confirmBrokerOrder.json"

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

    def test_confirm_success(self):
        """
        确认成交成功，购车证明和到店证明都上传图片
        校验点：1、data返回true
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {1: "确认成交成功，购车证明和到店证明都上传图片"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key - 1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))
            # 造数据，如果数据库中有这个单子，则删除后重新插入，用于确认成交
            sql_data = self.filecontent.get_sqldata(serial=key-1)
            if SqlOperation().select_data(sql_data['select_broker']) is not None:
                SqlOperation().delete_data(sql_data['delete_broker'])
            if SqlOperation().select_data(sql_data['select_oper']) is not None:
                SqlOperation().delete_data(sql_data['delete_oper'])
            SqlOperation().insert_data(sql_data['insert'])

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

            print("data verify is beginning...")
            self.verify.verify_data(expectresult=expectresult, result=json_result)
            print("data verify is success.")

            print("ALL END!!")

    def test_confirm_success_nopic(self):
        """
        确认成交成功，未上传图片
        校验点：1、message:返回值 没有附件信息,请重新上传
        :return: 
        """
        time.sleep(2)
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {2: "确认成交成功，不上传图片"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key - 1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))
            sql_data = self.filecontent.get_sqldata(serial=key - 1)
            if SqlOperation().select_data(sql_data['select_broker']) is not None:
                SqlOperation().delete_data(sql_data['delete_broker'])
            if SqlOperation().select_data(sql_data['select_oper']) is not None:
                SqlOperation().delete_data(sql_data['delete_oper'])
            SqlOperation().insert_data(sql_data['insert'])

            response = self.get_response(serial=key - 1)
            json_result = response.json()
            print(json_result)
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key - 1)

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)
            print("code verify is success.")

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)
            print("message verify is success.")

            print("ALL END!!")

    def test_order_status_changed(self):
        """
        当提交成交确认时，订单状态发生变更，message提示
        校验点：1、message:返回值 订单状态已变更,请刷新后重试
        :return: 
        """
        # 设置等待时间，防止并发访问接口
        time.sleep(4)
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {3: "订单状态发生变更，提示信息"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key - 1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))
            sql_data = self.filecontent.get_sqldata(serial=key-1)
            """
            if SqlOperation().select_data(sql_data['select']) == 0:
                SqlOperation().insert_data(sql_data['insert'])
            """
            SqlOperation().update_data(sql_data['update'])
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

            print("ALL END!!")

    def tearDown(self):
        SqlOperation().close()

if __name__ == '__main__':
    unittest.main()

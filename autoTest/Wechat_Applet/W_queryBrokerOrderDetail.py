# coding=utf-8

# coding=utf-8

import requests
import unittest
import operator
from Public.FileContent import FileContent
from Public.Request import Request
from Public.Verify import Verify
from Public.SqlOperation import SqlOperation


class QueryBrokerOrderDetail(unittest.TestCase):
    def setUp(self):
        self.filename = Request().dirname() + "/Document/Wechat_Applet/queryBrokerOrderDetail.json"

        self.filecontent = FileContent(self.filename)
        self.apiname = self.filecontent.get_apiname()  # 获取apiname用于获得url
        self.api = self.filecontent.get_api()  # 获取api用于校验
        self.caselist = self.filecontent.get_caselist()  # 获取caselist列表，包括"reqParams"和"expectResult"
        # self.casenumber = self.filecontent.get_casenumber()       # 获取case数量

        self.verify = Verify()
        # self.result = GlobalVar().global_dic
        # self.verificationErrors = []

    def get_response(self, serial):
        """

        :param serial:
        :return: 获取接口返回
        """
        url = Request().get_url(serial=serial, filename=self.filename, apiname=self.apiname)
        session = requests.session()
        response = session.post(url)
        return response

    def verify_status(self, serial, result):
        """
        校验status随着交易状态的改变而改变
        :return: 
        """
        expect_data = self.filecontent.get_expectresult(serial)['data']
        result_data = result['data']
        self.assertEqual(expect_data['status'], result_data['status'], msg="The status is not Equal.")

    def verify_operStepDesc(self, serial, result):
        """
        校验operStepDesc文案，这是用于显示在前端的
        :return: 
        """
        expect_oper = self.filecontent.get_data(serial)['tradeOrderOperLogResponses']
        print("expect_oper: ", expect_oper)
        result_oper = result['data']['tradeOrderOperLogResponses']
        expect_operStepDesc_list, result_operStepDesc_list = [], []
        if len(expect_oper) == len(result_oper):
            for i in range(len(expect_oper)):
                expect_operStepDesc_list.append(expect_oper[i]['operStepDesc'])
                result_operStepDesc_list.append(result_oper[i]['operStepDesc'])
        else:
            raise ValueError("length expect: {}, length result: {}".format(len(expect_oper), len(result_oper)))
        self.assertEqual(expect_operStepDesc_list, result_operStepDesc_list,
                         msg="tradeOrderOperLogResponses's operStepDesc is not Equal.")

    def test_begin_trade(self):
        """
        订单详情--经纪人发起交易
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {1: "订单详情--经纪人发起交易"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key-1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key-1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key-1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))
            sql_data = self.filecontent.get_sqldata(serial=key-1)
            if SqlOperation().select_data(sql_data['select']) is None:
                SqlOperation().insert_data(sql_data['insert'])
            else:
                SqlOperation().delete_data(sql_data['delete'])
                SqlOperation().insert_data(sql_data['insert'])
            response = self.get_response(serial=key-1)
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

            print("data verify is beginning...")
            self.verify.verify_data(expectresult=expectresult, result=json_result)
            print("data verify is success.")

            self.verify_status(serial=key-1, result=json_result)
            self.verify_operStepDesc(serial=key-1, result=json_result)

            print("ALL END!!")

    def tearDown(self):
        SqlOperation().close()


if __name__ == '__main__':
    unittest.main()

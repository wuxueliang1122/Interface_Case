# coding=utf-8

import requests
import unittest
import operator
from Public.FileContent import FileContent
from Public.Request import Request
from Public.Verify import Verify
from Public.SqlOperation import SqlOperation


class SaveCustomerServiceHandle(unittest.TestCase):
    def setUp(self):
        self.filename = Request().dirname() + "/Document/Wechat_Applet/saveCustomerServiceHandle.json"

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

    def verify_oper_step_sql(self, serial):
        """
        校验oper_step_desc=经纪人申请申诉
        :param serial: 
        :return: 
        """
        select_sql = self.filecontent.get_sqldata(serial)['select_oper']
        oper_step_desc = SqlOperation().select_data(select_sql)
        self.assertIsNotNone(oper_step_desc,
                             msg="经纪人申请申述后，trans.trade_oper_log表中oper_step_desc!='经纪人申请申诉'")

    def test_get_success(self):
        """
        经纪人客服申诉成功
        校验点：1、message:返回值 success
               2、申述成功后，trans.trade_oper_log多了一条记录，oper_step_desc=经纪人申请申诉
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {1: "经纪人客服申诉成功"}
        for key, value in casenum.items():
            # print(value, self.filecontent.get_instruction(serial=key-1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))
            """
            判断trans.trade_order_broker表订单车商是否申请退款refund_status=1，如果不是，则删除重新插入车商申请退款的订单；
            再判断trans.trade_oper_log表oper_step_desc是否存在“经纪人申请申诉”，如果有的话则删除，防止重复用此订单出现多个申述记录
            """
            sql_data = self.filecontent.get_sqldata(serial=key - 1)
            if SqlOperation().select_data(sql_data['select_broker']) is None:
                SqlOperation().delete_data(sql_data['delete_broker'])
                SqlOperation().insert_data(sql_data['insert'])
            if SqlOperation().select_data(sql_data['select_oper']) is not None:
                SqlOperation().delete_data(sql_data['delete_oper'])
            response = self.get_response(serial=key - 1)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key - 1)

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)

            self.verify_oper_step_sql(serial=key-1)

            print("ALL END!!")

    def tearDown(self):
        SqlOperation().close()


if __name__ == '__main__':
    unittest.main()

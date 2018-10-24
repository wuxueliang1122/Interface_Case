# coding=utf-8

import requests
import unittest
import operator
import time
from Public.FileContent import FileContent
from Public.Request import Request
from Public.Verify import Verify
from Public.SqlOperation import SqlOperation


class AgreeRefundBrokerOrder(unittest.TestCase):
    def setUp(self):
        self.filename = Request().dirname() + "/Document/Wechat_Applet/agreeRefundBrokerOrder.json"

        self.filecontent = FileContent(self.filename)
        self.apiname = self.filecontent.get_apiname()  # 获取apiname用于获得url
        self.api = self.filecontent.get_api()  # 获取api用于校验
        self.caselist = self.filecontent.get_caselist()  # 获取caselist列表，包括"reqParams"和"expectResult"

        self.verify = Verify()
        # self.result = GlobalVar().global_dic
        self.verificationErrors = []

    def get_response(self, serial):
        """
        因为reqParams请求参数需要用到变量即order_no是随机生成的，所以这里需要单独生成请求参数
        :param serial:
        :return: 获取接口返回
        """
        params = self.filecontent.get_reqparams(serial)
        params['agreeInfo']['orderNo'] = self.get_order_no()
        print("order_no: ", self.get_order_no())
        url = Request().get_url_params(params=params, apiname=self.apiname)
        response = requests.post(url)
        if response.status_code == 200:
            return response
        else:
            raise ConnectionRefusedError("request is refused.")

    @ staticmethod
    def get_order_no():
        """
        因为涉及到打款，cgpay那边有订单号的记录，所以这边的order_no不能用重复的，不然会打款失败，回调会false，同意退款就失败了
        order_no格式：YJD20180919180020000003，YJD + 年月日时分秒 + 888888
        :return: 
        """
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        num = '888888'
        order_no = "YJD" + now_time + num
        print(order_no)
        return order_no

    def verify_oper_step_sql(self, serial):
        """
        校验oper_step_desc=经纪人同意退款
        :param serial: 
        :return: 
        """
        select_sql = self.filecontent.get_sqldata(serial)['select_oper']
        oper_step_desc = SqlOperation().select_data(select_sql)
        self.assertIsNotNone(oper_step_desc,
                             msg="经纪人同意退款后后，trans.trade_oper_log表中oper_step_desc!='经纪人同意退款'")

    def test_agree_refund(self):
        """
        经纪人同意退款
        校验点：1、message: 返回值 同意退款成功
               2、经纪人同意退款后，trans.trade_oper_log多了一条记录，oper_step_desc=经纪人同意退款
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {1: "车商支付成功后申请退款，经纪人同意退款"}
        for key, value in casenum.items():
            # print(value, self.filecontent.get_instruction(serial=key-1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

            """
            在get_order_no函数中已经判断过order_no在数据库中是不存在的，所以只需要直接insert即可
            """
            sql_data = self.filecontent.get_sqldata(serial=key - 1)
            insert = sql_data['insert'].format(self.get_order_no())
            print(insert)
            SqlOperation().insert_data(insert)

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

            self.verify_oper_step_sql(serial=key - 1)

            print("ALL END!!")

    def tearDown(self):
        SqlOperation().close()


if __name__ == '__main__':
    unittest.main()


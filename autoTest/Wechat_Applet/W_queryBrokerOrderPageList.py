# coding=utf-8
import unittest
import requests
import operator
from Public.FileContent import FileContent
from Public.Request import Request
from Public.Verify import Verify
from Public.SqlOperation import SqlOperation


class QueryBrokerOrderPageList(unittest.TestCase):
    def setUp(self):
        self.filename = Request().dirname() + "/Document/Wechat_Applet/queryBrokerOrderPageList.json"

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
        if response.status_code == 200:
            return response
        else:
            raise ConnectionRefusedError()

    def verify_datalist_number(self, serial, result):
        """
        校验dataList列表长度，小于等于pagesize，即每次请求最多为pagesize规定的数值，默认为15
        :return: 
        """
        pagesize_parama = self.filecontent.get_reqparams(serial)['queryRequest']['pagesize']
        datalist = result['data']['dataList']
        len_datalist = len(datalist)
        self.assertTrue(len_datalist <= pagesize_parama,
                        msg="len_datalist: {}, pagesize: {}".format(len_datalist, pagesize_parama))

    def verify_status(self, serial, result):
        """
        校验status为当前查询列表的status
        :param serial: 
        :param result: 
        :return: 
        """
        expect_status = self.filecontent.get_datalist(serial)[0]['status']
        result_datalist = result['data']['dataList']
        for i in range(len(result_datalist)):
            self.assertEqual(expect_status, result_datalist[i]['status'])

    def test_to_pay(self):
        """
        待车商支付订单列表
        校验点：1、校验datalist列表长度<=pagesize的值
               2、校验datalist所有订单的status=0
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {1: "待车商支付订单列表"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key-1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key-1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key-1)))
            else:
                raise ValueError("TestCase {}'s instruction is not Equal to CaseNum.".format(key-1))
            sql_data = self.filecontent.get_sqldata(serial=key-1)
            if SqlOperation().select_data(sql_data['select']) != 0:
                SqlOperation().delete_data(sql_data['delete'])
            SqlOperation().insert_data(sql_data['insert'])
            response = self.get_response(serial=key-1)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key-1)

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)
            print("code verify is success.")

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)
            print("message verify is success.")

            self.verify_datalist_number(serial=key - 1, result=json_result)
            self.verify_status(serial=key-1, result=json_result)

            print("ALL END!!")

    def test_broker_to_confirm(self):
        """
        待经纪人确认订单列表
        校验点：1、校验datalist列表长度<=pagesize的值
               2、校验datalist所有订单的status=1
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {2: "待经纪人确认订单列表"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key - 1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("TestCase {}'s instruction is not Equal to CaseNum.".format(key - 1))
            sql_data = self.filecontent.get_sqldata(serial=key - 1)
            if SqlOperation().select_data(sql_data['select']) != 0:
                SqlOperation().delete_data(sql_data['delete'])
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

            self.verify_datalist_number(serial=key - 1, result=json_result)
            self.verify_status(serial=key - 1, result=json_result)

            print("ALL END!!")

    def test_customer_to_confirm(self):
        """
        待车商确认订单列表
        校验点：1、校验datalist列表长度<=pagesize的值
               2、校验datalist所有订单的status=2
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {3: "待车商确认订单列表"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key - 1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("TestCase {}'s instruction is not Equal to CaseNum.".format(key - 1))
            sql_data = self.filecontent.get_sqldata(serial=key - 1)
            if SqlOperation().select_data(sql_data['select']) is not None:
                SqlOperation().delete_data(sql_data['delete'])
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

            self.verify_datalist_number(serial=key - 1, result=json_result)
            self.verify_status(serial=key - 1, result=json_result)

            print("ALL END!!")

    def test_paid_success(self):
        """
        交易成功订单列表
        校验点：1、校验datalist列表长度<=pagesize的值；
               2、校验datalist所有订单的status=3
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {4: "交易成功订单列表"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key-1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key-1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key-1)))
            else:
                raise ValueError("TestCase {}'s instruction is not Equal to CaseNum.".format(key-1))
            response = self.get_response(serial=key-1)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key-1)

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)
            print("code verify is success.")

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)
            print("message verify is success.")

            self.verify_datalist_number(serial=key - 1, result=json_result)
            self.verify_status(serial=key-1, result=json_result)

            print("ALL END!!")

    def test_paid_fail(self):
        """
        交易失败订单列表
        校验点：1、校验datalist列表长度<=pagesize的值
               2、校验datalist所有订单的status=3
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {5: "交易失败订单列表"}
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

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)
            print("code verify is success.")

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)
            print("message verify is success.")

            self.verify_datalist_number(serial=key - 1, result=json_result)
            self.verify_status(serial=key - 1, result=json_result)

            print("ALL END!!")

    def test_all_list(self):
        """
        全部订单列表
        校验点：1、校验datalist列表长度<=pagesize的值
               2、datalist不为空
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {6: "全部订单列表"}
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

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)
            print("code verify is success.")

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)
            print("message verify is success.")

            self.verify_datalist_number(serial=key-1, result=json_result)
            self.verify.verify_data_isNotNull(result=json_result)

            print("ALL END!!")

    def tearDown(self):
        SqlOperation().close()


if __name__ == '__main__':
    unittest.main()

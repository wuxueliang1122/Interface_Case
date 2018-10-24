# coding=utf-8
import unittest
import requests
import operator
from Public.FileContent import FileContent
from Public.Request import Request
from Public.Verify import Verify
from Public.SqlOperation import SqlOperation


class GetVirtualOrderList(unittest.TestCase):
    def setUp(self):
        self.filename = Request().dirname() + "/Document/Wechat_Applet/getVirtualOrderList.json"

        self.filecontent = FileContent(self.filename)
        self.apiname = self.filecontent.get_apiname()  # 获取apiname用于获得url
        self.api = self.filecontent.get_api()  # 获取api用于校验
        self.caselist = self.filecontent.get_caselist()  # 获取caselist列表，包括"reqParams"和"expectResult"
        # self.casenumber = self.filecontent.get_casenumber()       # 获取case数量

        self.verify = Verify()
        self.verificationErrors = []

        delete_sql = "DELETE FROM trans.trade_announcement_order"
        SqlOperation().delete_data(delete_sql)

    def get_response(self, serial):
        """

        :param serial:
        :return: 获取接口返回
        """
        if 'sql' in self.filecontent.get_caselist()[serial]:
            SqlOperation().insert_data(self.json_converto_sql(serial))
        url = Request().get_url(serial=serial, filename=self.filename, apiname=self.apiname)
        response = requests.post(url)
        return response

    def json_converto_sql(self, serial):
        """
        从json文件读取json格式的sql语句并转换为sql语句,只适用本脚本，如果数据表增加列了，这里也需要增加
        :param serial:
        :return:
        """
        sql_data = self.filecontent.get_sqldata(serial)
        print("sql_data: ", sql_data)
        sql = "\r\n" + "INSERT INTO trans.trade_announcement_order " \
                       "(id, order_no, broker_name, create_time, modify_time, commission_amount, source) VALUES \r\n"
        for i in range(len(sql_data)):
            data = sql_data[i]
            if i < len(sql_data) - 1:
                sql = sql + "('%s', '%s', '%s', '%s', '%s', '%s', '%s'),\r\n" % (
                                                                    data['id'], data['order_no'], data['broker_name'],
                                                                    data['create_time'], data['modify_time'],
                                                                    data['commission_amount'], data['source'])
            else:
                sql = sql + "('%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
                    data['id'], data['order_no'], data['broker_name'],
                    data['create_time'], data['modify_time'],
                    data['commission_amount'], data['source'])
        print(sql)
        return sql

    def test_virtualorder_isNull(self):
        """
        当虚拟订单池为空，即虚拟订单数据库为空
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {1: "当虚拟订单池为空，即虚拟订单数据库为空"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key-1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key-1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key-1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

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

            print("ALL END!!")

    def test_get_virtualorder(self):
        """
        当虚拟订单池为空，即虚拟订单数据库为空
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {2: "当虚拟订单池中有数据，获取虚拟订单信息"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key-1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key-1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key-1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

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

            print("ALL END!!")

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

# coding=utf-8

import requests
import unittest
import operator
from Public.FileContent import FileContent
from Public.Request import Request
from Public.Verify import Verify


class BrokerGetCarSourceDetail(unittest.TestCase):
    def setUp(self):
        self.filename = Request().dirname() + "/Document/Wechat_Applet/unBindCard.json"

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
            print(type(response))
            return response
        else:
            raise ConnectionRefusedError("request is refused.")

    def test_unbind_success(self):
        """
        解绑银行卡,不管银行卡在数据库中是否存在，接口没做匹配，因为肯定是从list列表做的操作
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {1: "解绑银行卡,不管银行卡在数据库中是否存在，接口没做匹配，因为肯定是从list列表做的操作"}
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

            print("ALL END!!")

    def check_sql(self):
        """
        可以查找数据库，解绑后数据库记录就没了，但是我现在没法区分车商钱包和经纪人钱包
        :return: 
        """
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

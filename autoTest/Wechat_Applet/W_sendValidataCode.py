# coding=utf-8
import unittest
import requests
import operator
import time
from Public.FileContent import FileContent
from Public.Request import Request
from Public.Verify import Verify
from Public.SqlOperation import SqlOperation


class SendValidataCode(unittest.TestCase):

    def setUp(self):
        self.filename = Request().dirname() + "/Document/Wechat_Applet/sendValidataCode.json"

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
        print(self.apiname)
        url = Request().get_url(serial=serial, filename=self.filename, apiname=self.apiname)
        # session = requests.session()
        response = requests.post(url)
        if response.status_code == 200:
            return response
        else:
            raise ConnectionRefusedError()

    def verify_received_mysql(self, serial):
        """
        校验数据库收到了验证码，只判断了最近的一条记录是发送的号码(号码从case获取)
        :param serial
        :return: 
        """
        sql = "SELECT * FROM auto.sms WHERE phone='{}' AND smstype='brokerUserLoginCode'"\
            .format(self.filecontent.get_reqparams(serial)['phone'])
        self.assertIsNotNone(SqlOperation().select_data(sql))

    def test_send_success(self):
        """
        成功发送验证码
        校验点：1、message:返回验证码已发送
               2、数据库收到了验证码
        :return: 
        """
        time.sleep(60)
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {1: "验证码已发送，成功发送验证码"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key - 1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("TestCase {}'s instruction is not Equal to CaseNum.".format(key - 1))

            delete_sql = """
                                    DELETE FROM auto.sms WHERE phone='{}'
                            """.format(self.filecontent.get_reqparams(serial=key-1)['phone'])
            SqlOperation().delete_data(sql=delete_sql)
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

            self.verify_received_mysql(serial=key-1)

            print("ALL END!!")

    def test_repeat_fail(self):
        """
        60s内仅能获取一次验证码
        校验点：1、message:60s内仅能获取一次验证码，请稍后再试
               2、code:返回值为20000
        :return: 
        """
        time.sleep(60)
        for num in range(len(self.caselist)):
            print("TestCase {}: {}".format((num + 1), self.filecontent.get_instruction(serial=num)))
            try:
                operator.eq(self.caselist[num]['serial'], num + 1)
            except IOError:
                print("TestCase Number: {} Document is ERROR!".format(num + 1))
            finally:
                self.filecontent.get_instruction(serial=num)
                response = self.get_response(serial=num)
                json_result = response.json()
                print("response content: ", json_result)
                expectresult = self.filecontent.get_expectresult(serial=num)

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
        SqlOperation().close()


if __name__ == '__main__':
    unittest.main()

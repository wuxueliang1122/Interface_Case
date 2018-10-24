# coding=utf-8

import unittest
import requests
import operator
import time
from Public.Request import Request
from Public.Verify import Verify
from Public.SqlOperation import SqlOperation
from Public.MD5 import MD5
from Public.MapUtil import MapUtil
from Public.FileContent import FileContent


class BrokerVerifyCodeLogin(unittest.TestCase):

    def setUp(self):
        self.filename = Request().dirname() + "/Document/Wechat_Applet/brokerVerifyCodeLogin.json"
        # self.filename = os.path.abspath("../Document/Wechat_Applet/brokerVerifyCodeLogin")

        self.filecontent = FileContent(self.filename)
        self.apiname = self.filecontent.get_apiname()
        self.api = self.filecontent.get_api()
        self.caselist = self.filecontent.get_caselist()

        self.verify = Verify()

        self.phone = "18867520068"

    def get_url(self, requestparam):
        """
        创建会话，获取response
        :param requestparam:
        :return:
        """
        dic = dict()
        dic['requestParam'] = requestparam
        dic['source'] = int(Request().get_source())
        signature = MD5().encodingpassword(MapUtil().get_signbase(dic, Request.separator()) +
                                           MD5().encodingpassword(Request.get_app_secret()))
        dic["signature"] = signature
        url = Request().get_host() + self.apiname + "?" + MapUtil().get_signbase(dic, Request.separator())
        print("url: ", url)
        return url

    def get_success_response(self):
        """
        serial为0时，获取验证码登陆
        :param serial:
        :return:
        """
        requestParam = {
            "cellphone": self.phone,
            "verifyCode": self.get_verify_code(),
            "code": ""
        }
        response = requests.post(self.get_url(requestParam))
        return response

    def get_response(self, serial):
        """
        从json文件中读取请求参数
        :param serial:
        :return:
        """
        url = Request().get_url(serial=serial, apiname=self.apiname, filename=self.filename)
        response = requests.post(url)
        if response.status_code == 200:
            return response
        else:
            raise ConnectionRefusedError()

    @staticmethod
    def sendvaliddatacode():
        """
        sendValiddataCode
        :return:
        """
        reqparams = "http://10.10.13.75:8080/dealer/sendvalidatecode.json?" \
                    "invokeType=20&phone=18867520068&signature=589f9e341eca8079f33e80adb3b7b3b3&source=123456"
        # sendvalidatacode_url = Request().get_host() + self.apiname + "?" + reqparams
        r = requests.post(url=reqparams)
        if r.json()['message'] == "验证码已发送":
            print("验证码已发送")
        else:
            print("sendValidataCode response is ", r.json())
            raise ConnectionError("The api sendValidataCode response is error. %s" % r.json())

    def get_verify_code(self):
        time.sleep(60)
        self.sendvaliddatacode()
        sql = """
                SELECT code FROM auto.sms WHERE phone='18867520068' AND smstype='brokerUserLoginCode' 
                ORDER BY sendtime DESC LIMIT 1
            """
        code = SqlOperation().select_data(sql=sql)[0]
        if len(code) == 6:
            print("get verify code is ", code)
            return code
        else:
            raise ValueError("The verify code is Error. Please check the sendvalidatacode api is OK.", code)

    def test_login_success(self):
        print("TestCase 1:")
        json_result = self.get_success_response().json()
        expectresult = self.filecontent.get_expectresult(serial=0)
        print("result: ", json_result)
        self.assertEqual(expectresult['code'], json_result['code'], msg="Code is Error, result = %s."
                                                                        % json_result)
        self.assertEqual(expectresult['message'], json_result['message'], msg="Message is Error, result = %s."
                                                                              % json_result['message'])
        self.assertEqual(expectresult['data'], json_result['data'],
                         msg="Data is Error, result = {}." .format(json_result))
        print("Test Login Success is OK.")

    def test_login_fail(self):
        """
        登陆失败，验证码过期
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {2: "登陆失败，验证码过期/错误"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key-1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key-1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key-1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

            delete_sql = """
                                                DELETE FROM auto.sms WHERE phone='{}'
                                        """.format(self.filecontent.get_reqparams(serial=key - 1)['phone'])
            SqlOperation().delete_data(sql=delete_sql)

            response = self.get_response(serial=key-1)
            self.verify.verify_code_200(response=response)
            print(response.content)
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

            print("ALL END!!")

    def tearDown(self):
        SqlOperation().close()

if __name__ == '__main__':
    unittest.main()


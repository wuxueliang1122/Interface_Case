# coding=utf-8


import unittest
import requests
import operator
from Public.Request import Request
from Public.FileContent import FileContent
from Public.Verify import Verify


class CanPublishBrokerCarsrcList(unittest.TestCase):

    def setUp(self):
        self.filename = Request().dirname() + "/Document/B_Client/canPublishBrokerCarsrcList.json"

        self.filecontent = FileContent(self.filename)
        self.apiname = self.filecontent.get_apiname()
        self.api = self.filecontent.get_api()
        self.caselist = self.filecontent.get_caselist()

        self.verify = Verify()

        self.verificationError = []

    def get_response(self, serial):
        url = Request().get_url(serial=serial, filename=self.filename, apiname=self.apiname)
        session = requests.session()
        response = session.post(url)
        if response.status_code == 200:
            return response
        else:
            raise ConnectionRefusedError()

    def verify_publishBrokerStatus(self, serial, result):
        """
        校验response.datalist.publishBrokerStatus == expectResult.dataList.publishBrokerStatus
        :param serial: 
        :param result: 
        :return: 
        """
        param_datalist = self.filecontent.get_datalist(serial)
        param_status = []
        for i in range(len(param_datalist)):
            status = param_datalist[i]['publishBrokerStatus']
            if status not in param_status:
                param_status.append(status)
        for data in result['data']['dataList']:
            self.assertIn(data['publishBrokerStatus'], param_status,
                          msg="The result dataList contains publishBrokerStatus {} != {}"
                          .format(data['publishBrokerStatus'], param_status))

    def test_search_unrelease(self):
        """
        未发布车源，查询成功
        校验点：1、publishBrokerStatus，注意未发布状态请求参数publishBrokerStatus=2，而返回结果publishBrokerStatus=0 or 2
        请求结果在数据库company_car_source_order:`publish_broker_status`'发布到经纪人状态(0:未发布, 1: 发布, 2: 取消)',
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {1: "未发布"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key-1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key-1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key-1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

            response = self.get_response(serial=key-1)
            self.verify.verify_code_200(response=response)
            print(response.content)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key-1)

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)
            print("code verify is success.")

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)
            print("message verify is success.")

            self.verify_publishBrokerStatus(serial=key - 1, result=json_result)

            print("ALL END!!")

    def test_search_release(self):
        """
        已发布车源，查询成功
        :return: 
        """
        # casenum = {serial: instruction}, 如果与json文档不一致的话就会报错
        casenum = {2: "已发布"}
        for key, value in casenum.items():
            print(value, self.filecontent.get_instruction(serial=key - 1))
            if operator.eq(value, self.filecontent.get_instruction(serial=key - 1)):
                print("TestCase {}: {}".format(key, self.filecontent.get_instruction(serial=key - 1)))
            else:
                raise ValueError("用例匹配失败：TestCase {}'s instruction is not Equal to CaseNum.".format(key))

            response = self.get_response(serial=key - 1)
            self.verify.verify_code_200(response=response)
            print(response.content)
            json_result = response.json()
            print("response content: ", json_result)
            expectresult = self.filecontent.get_expectresult(serial=key - 1)

            print("code verify is beginning...")
            self.verify.verify_code(expectresult=expectresult, result=json_result)
            print("code verify is success.")

            print("message verify is beginning...")
            self.verify.verify_message(expectresult=expectresult, result=json_result)
            print("message verify is success.")

            self.verify_publishBrokerStatus(serial=key - 1, result=json_result)

            print("ALL END!!")

if __name__ == '__main__':
    unittest.main()

# coding=utf-8

import unittest
import operator
from Public.CmpStructrue import CmpStructrue


class Verify(unittest.TestCase):

    def setUp(self):
        self.verificationError = []

    def verify_code_200(self, response):
        self.assertEqual(200, response.status_code,
                         msg="verify_code_200: The api connection code is not 200, r.code_status{}."
                             .format(response.status_code))

    def verify_api(self, expectresult, result):
        """
        校验接口返回信息中的apiname与校验文本中是否一致，如果返回内容为空，那么就直接抛出异常，接口应该有问题了
        :param expectresult:json文档中用于校验的api
        :param result:
        :return:
        """
        # 如果接口返回为空，那说明接口有问题，直接抛出异常
        if len(result) == 0:
            raise ConnectionError("verify_apiname: The response content maybe NULL.")
        else:
            if 'api' in expectresult.keys():
                self.assertEqual(expectresult['api'], result['api'],
                                 msg="verify_apiname: the apiname {} of response is not same.".format(result))
            else:
                pass

    def verify_code(self, expectresult, result):
        """
        校验code的value值
        :param expectresult: json文档中用于校验的标准内容
        :param result:
        :return:
        """
        if 'code' in expectresult.keys():
            self.assertEqual(int(expectresult['code']), int(result['code']),
                             msg="verify_code: The response code is {}.".format(result['code']))
        else:
            raise IOError("verify_code: The code maybe NULL, please check the json document.")

    def verify_message(self, expectresult, result):
        """
        校验message的value值
        :param expectresult:
        :param result:
        :return:
        """
        if 'message' in expectresult.keys():
            self.assertEqual(expectresult['message'], result['message'],
                             msg="verify_message: The response message is {}.".format(result['message']))
        else:
            pass

    def verify_data(self, expectresult, result):
        """
        接口返回内容中data字段的校验，现在主要是对data的key值进行校验，只要key值保持一致即可。
        :param expectresult:
        :param result:
        :return:
        """
        types = [dict, list, tuple]
        if 'data' in expectresult.keys():
            if type(expectresult['data']) in types:
                try:
                    if type(expectresult['data']) is dict:
                        self.assertEqual(len(expectresult['data']), len(result['data']))
                    elif type(expectresult['data']) is list or type(expectresult['data']) is tuple:
                        for i in range(len(expectresult['data'])):
                            self.assertEqual(expectresult['data'][i], result['data'][i])
                except IOError:
                    print("verify_data: Length is not Equal. The length of expectresult is {}, "
                          "and the length of response data is {}.".format(len(expectresult['data']), len(result['data'])))
                if len(expectresult['data']) != 0:
                    self.assertTrue(CmpStructrue().cmp_object(expectresult['data'], result['data']))
                else:
                    self.assertEqual(expectresult['data'], result['data'],
                                     msg="Data verify is Error.")
            else:
                self.assertEqual(expectresult['data'], result['data'])
        else:
            pass

    def verify_datalist(self, expectresult, result):
        """
        如果dataList为空，比较是否为空
        :param expectresult:
        :param result:
        :return:
        """
        if 'data' in expectresult:
            if 'dataList' in expectresult['data'] and expectresult['data']['dataList'] == []:
                print("verify_dataList")
                self.assertEqual(expectresult['data']['dataList'], result['data']['dataList'],
                                 msg="The dataList is error.")
            else:
                print("The data don't contain dataList.")
        else:
            pass

    def verify_data_isNotNull(self, result):
        """
        data列表不为空
        :param result: 
        :return: 
        """
        self.assertIsNotNone(result['data'], msg="result data is NULL.")

    def tearDown(self):
        self.assertEqual([], self.verificationError,
                         msg="tearDown: the verificationError: {}".format(self.verificationError))

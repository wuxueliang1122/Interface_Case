# coding=utf-8

from Public.MapUtil import MapUtil as maputil
from Public.MD5 import MD5
from Public.FileContent import FileContent
import os


class Request:

    @ staticmethod
    def get_source(source=''):
        return source

    @ staticmethod
    def get_app_secret(app_secret=''):
        return app_secret

    @ staticmethod
    def get_host(host=""):
        """app的host地址"""
        return host

    @ staticmethod
    def get_manage_host(host=""):
        """管理后台的host地址"""
        return host

    @ staticmethod
    def separator():
        return "&"

    @ staticmethod
    def dirname():
        return os.getcwd()

    def __init__(self):
        self.source = self.get_source()
        self.app_secret = self.get_app_secret()
        self.host = self.get_host()
        self.manage_host = self.get_manage_host()
        self.separator = Request.separator()

    def get_url_params(self, params, apiname):
        """
        :return:生成请求的url，请求参数中有值需要在函数中写入
        """
        params['source'] = self.source

        # 把source存入字典用于后续签名认证，格式source:123456
        # 把signature存入字典用于转换为url字符串，格式signature:1234567890
        signature = MD5().encodingpassword(maputil.get_signbase(params, self.separator) +
                                           MD5().encodingpassword(self.app_secret))
        params['signature'] = signature
        # 生成request_url
        url = self.host + apiname + "?" + maputil.get_signbase(params, self.separator)

        print("url:", url)
        return url

    def get_url(self, serial, filename, apiname):
        """
        请求参数在json文档中写死的
        :param serial: 
        :param filename: 
        :param apiname: 
        :return: 拼接完成用于请求的url
        """
        params = FileContent(filename).get_reqparams(serial)
        params['source'] = self.source

        # 把source存入字典用于后续签名认证，格式source:123456
        # 把signature存入字典用于转换为url字符串，格式signature:1234567890
        signature = MD5().encodingpassword(maputil.get_signbase(params, self.separator) +
                                           MD5().encodingpassword(self.app_secret))
        params['signature'] = signature
        # 生成request_url
        url = self.host + apiname + "?" + maputil.get_signbase(params, self.separator)

        print("url:", url)
        return url

    def get_manage_url(self, serial, filename, apiname):
        """
        请求参数在json文档中写死的
        :param serial: 
        :param filename: 
        :param apiname: 
        :return: 
        """
        params = FileContent(filename).get_reqparams(serial)
        params['source'] = self.source

        # 把source存入字典用于后续签名认证，格式source:123456
        # 把signature存入字典用于转换为url字符串，格式signature:1234567890
        signature = MD5().encodingpassword(maputil.get_signbase(params, self.separator) +
                                           MD5().encodingpassword(self.app_secret))
        params['signature'] = signature
        # 生成request_url
        url = self.manage_host + apiname + "?" + maputil.get_signbase(params, self.separator)

        print("url:", url)
        return url

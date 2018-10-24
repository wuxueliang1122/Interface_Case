# coding=utf-8

from urllib import parse
import re


class MapUtil:

    @staticmethod
    def get_signbase(dic, separator):
        """
        :dic: 用于转换的字典，包括source、params
        :separator:连接符
        :return:获取用于转换成md5的字符串 
        """
        buffer = []
        for key in sorted(dic.keys()):
            buffer.append("%s=%s" % (key, dic[key]))
        return separator.join(buffer)

    def get_urlencode(self, dic, separator, source, signature):
        """
        没调用到，发现还是url编码还是有问题
        :param dic: 
        :param separator: 
        :param source
        :param signature
        :return: 如果请求参数带中文，返回转码后的字符串用于拼接url
        """
        zhpattern = re.compile(u'[\u4e00-\u9fa5]+')
        dict_buff = {}
        buff = {}
        for key, value in dic.items():
            if type(value) == dict:
                for k, v in value.items():
                    if type(v) is not int:
                        if zhpattern.search(v):
                            dict_buff[k] = parse.quote(v)
                        else:
                            dict_buff[k] = v
                    else:
                        dict_buff[k] = v
            buff[key] = dict_buff
        return self.get_signbase(buff, separator) + "&signature={}&source={}".format(signature, source)

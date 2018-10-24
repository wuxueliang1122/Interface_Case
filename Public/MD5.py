# coding=utf-8

import hashlib


class MD5:

    @staticmethod
    def encodingpassword(password):
        """
        
        :param password: 字符串
        :return: md5值用作验签
        """
        md5 = hashlib.md5()
        md5.update(password.encode("utf-8"))
        return md5.hexdigest()

# coding=utf-8

import unittest
import time
import HTMLTestRunner
import os

base_dir = "D:\\Python-workplace\\cheguo_auto\\"


class RunTestCase:

    @staticmethod
    def testsuite():
        """
        构造测试集
        :return: 
        """
        listcase = base_dir + "cheguo_auto\\autoTest"
        testunits = unittest.TestSuite()
        patterns = ["W_*.py", "B_*.py", "P_*.py"]

        for pattern in patterns:
            discover = unittest.defaultTestLoader.discover(listcase,
                                                           pattern=pattern,
                                                           top_level_dir=None)

            for testcase in discover:
                testunits.addTest(testcase)
        return testunits


if __name__ == '__main__':

    now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))

    filename = base_dir + "cheguo_auto\\TestReports\\" + now_time + ".html"
    with open(filename, 'wb') as fp:

        runner = HTMLTestRunner.HTMLTestRunner(
            stream=fp,
            title="车国接口测试报告",
            description="测试用例运行情况")
        testunit = RunTestCase().testsuite()
        runner.run(testunit)

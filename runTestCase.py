# coding=utf-8

import unittest
import time
import HTMLTestRunner
import os
import sys

base_dir = os.getcwd()
listcase = base_dir + "Interface_case/autoTest"


class RunTestCase:

    @staticmethod
    def testsuite():
        """
        构造测试集
        :return: 
        """
        testunits = unittest.TestSuite()
        patterns = ["W_*.py", "B_*.py", "P_*.py"]

        for pattern in patterns:
            discover = unittest.defaultTestLoader.discover(listcase,
                                                           pattern=pattern,
                                                           top_level_dir=base_dir)

            for testcase in discover:
                testunits.addTest(testcase)
        return testunits


if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.getcwd()))
    now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))

    filename = base_dir + "/TestReports/" + now_time + ".html"
    print(filename)
    with open(filename, 'wb') as fp:

        runner = HTMLTestRunner.HTMLTestRunner(
            stream=fp,
            title="接口测试报告",
            description="测试用例运行情况")
        testunit = RunTestCase().testsuite()
        runner.run(testunit)

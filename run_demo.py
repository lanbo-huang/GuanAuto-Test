#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os,sys
sys.path.append(os.path.dirname(__file__))
import setting
import unittest,time
import sendmail
from newReport import new_report
from HTMLTestRunner import HTMLTestRunner

from ExceptHookHandler import ExceptHookHandler as ehh

def add_case(test_path=os.path.dirname(__file__)):
    """加载所有的测试用例"""
    discover = unittest.defaultTestLoader.discover(test_path, pattern='*case.py')
    return discover


def run_case(all_case,result_path=setting.TEST_REPORT):
    """执行所有的测试用例"""
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename =  result_path + '/' + now + 'result.html'
    with open(filename,'wb') as f:
        runner = HTMLTestRunner(stream=f,title='观系统pc接口自动化测试报告',
                            description='环境：windows 10 浏览器：chrome',
                            tester='HWY')
        runner.run(all_case)
    report = new_report(setting.TEST_REPORT) #取出最新的报告
    sendmail.send_mail(report) #调用发送邮件模块

if __name__ =="__main__":
    EHH = ehh()
    cases = add_case()

    #第一种用HTML形式跑测试用例
    #run_case(cases)

    #第二种直接用unittest框架自带方法跑,方便调试
    runner = unittest.TextTestRunner()
    runner.run(cases)

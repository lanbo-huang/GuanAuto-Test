#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'HWY'

import os,sys,json
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import unittest,requests,ddt
from readxls import ReadExcel
from send_request_h5 import SendRequests



testData = ReadExcel('yatong_h5.xlsx').read_data()#读取具体的xlsx文件，所有的api信息存储在这里


@ddt.ddt
class Guan_API(unittest.TestCase):
    """观-PC"""
    def setUp(self):
        self.s = requests.session()

    def tearDown(self):
        pass

    @ddt.data(*testData)
    def test_api(self,data):
        print("******* 正在执行用例 ->{0} *********".format(data['ID']))
        print("请求方式: {0}，请求URL: {1}".format(data['method'],data['url']))
        print("请求参数：{0}".format(data["params"]))
        print("post请求体data数据：{0}".format(data["data"]))
        # 发送请求
        re = SendRequests().sendRequests(self.s,data)
        # 获取服务端返回的值
        self.result = re.json()
        print("页面返回信息：%s" % re.content.decode("utf-8"))
        # 获取excel表格数据的状态码和消息
        readData_code = (data["status_code"])
        readData_msg = data["msg"]

        #判断获取的状态码与实际结果的状态码及返回信息是否一致
        if self.result["code"]==readData_code and self.result["msg"]==readData_msg:
            OK_data = "PASS"
            print("用例测试结果:  {0}---->{1}".format(data['UseCase'],OK_data))

        if self.result["code"]!=0 or self.result["msg"]!="OK":
            NOT_data = "FAIL"
            print("用例测试结果:  {0}---->{1}".format(data['UseCase'], NOT_data))

        self.assertEqual(self.result['code'], readData_code, "返回实际结果是->:%s" % self.result['code'])
        self.assertEqual(self.result['msg'], readData_msg, "返回实际结果是->:%s" % self.result['msg'])

if __name__=='__main__':
    unittest.main()

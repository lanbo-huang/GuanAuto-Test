#!/usr/bin/env python
import os,sys,json
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import unittest,requests,ddt
from readxls import ReadExcel
from send_request import SendRequests
from configparser import ConfigParser
from Depend import Depend
from log import common



#读取执行测试的接口
path = os.path.dirname(os.path.dirname(__file__))
filename =  path + '\Testapis\h5_in.xlsx'
testData = ReadExcel(filename).read_data()#以行的方式，读取具体的xlsx文件，所有的api信息存储在这里


#读取执行测试的环境及参数信息
cf = ConfigParser()
cf.read(path+"\config\config.ini",encoding="utf-8")
code = cf.get("host","code")
environment = cf.get("host","environment")
phone = cf.get("logintype","h5_out")




@ddt.ddt
class Guan_API(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
       cls.logs = common.Common().get_logs()
       cls.logs.debug('开始写入接口自动化测试用例')

    @classmethod
    def tearDownClass(cls):
        cls.logs.debug('自动化接口用例结束')


    def setUp(self):
        self.s = requests.session()

    def tearDown(self):
        pass

    @ddt.data(*testData)
    def test_api(self,datas):
        print("******* 正在执行用例 ->{0} *********".format(datas['ID']))
        print("请求方式：{0}".format(datas['method']))
        print("请求url：{0}".format(datas['url']))

        # 发送请求
        method = datas["method"]
        api = datas["url"]
        logintype = datas["logintype"]
        headertype = datas["headertype"]

        params = datas["params"]
        if params == "":
            params = None
        else:
            params = json.loads(params)

        data = datas["data"]
        if data == "":
            data =None
        else:
            data = json.loads(data)

        dependcase = datas["dependcase"]
        dependtype = datas["dependtype"]
        dependkey = datas["dependkey"]
        depend_result_key = datas["depend_result_key"]

        #判断是否需要跑依赖case
        if dependcase !="":
            if dependtype == "params":#参数依赖，参数依赖键值重新赋值
                res = Depend(filename,phone).get_depend_rundata(dependcase,depend_result_key)
                params[dependkey] = res
                #print(params)
            else:#data依赖，参数依赖键值重新赋值
                res = Depend(filename, phone).get_depend_rundata(dependcase, depend_result_key)
                data[dependkey] = res

        print("请求参数：{0}".format(params))
        print("请求体数据：{0}".format(data))
        re = SendRequests(environment,code,phone).newsendRequests(self.s,logintype,headertype,api,method,params,data)
        # 获取服务端返回的值
        self.result = re.json()
        print("返回结果：%s" % re.content.decode("utf-8"))

        # 获取excel表格数据的状态码和消息
        readData_code = datas["status_code"]
        readData_msg = datas["msg"]

        # 判断获取的状态码与实际结果的状态码及返回信息是否一致
        if self.result["code"] == readData_code and self.result["msg"] == readData_msg:
            OK_data = "PASS"
            print("用例测试结果:  {0}---->{1}".format(datas['UseCase'], OK_data))

        if self.result["code"] != 0 or self.result["msg"] != "OK":
            NOT_data = "FAIL"
            # breakpoint()
            print("用例测试结果:  {0}---->{1}".format(datas['UseCase'], NOT_data))

        self.assertEqual(self.result['code'], readData_code, "返回实际结果是->:%s" % self.result['code'])
        self.assertEqual(self.result['msg'], readData_msg, "返回实际结果是->:%s" % self.result['msg'])


if __name__=='__main__':
    unittest.main()

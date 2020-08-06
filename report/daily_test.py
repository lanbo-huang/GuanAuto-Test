import requests
import json
class Sendrquests():
    def __init__(self):
        self.url ="https://guan.yatonghui.com"
        self.api="/api/verification/code/1/"
        self.phone="17704034087"
        self.headers ={
            'Eaton-Origin': 'H5',
            'Eaton-Company-CODE': 'CSGS',
            'Content-Type': 'application/json;charset=UTF-8',
            'Eaton-ORG-ID': '1206346874605690882'  # 对应登录账户的权限ID
        }
        self.data={
            'phone':'17704034087',
            'code':'6666',
            'loginType':'2'
                }
        re = requests.get(url=self.url+self.api+self.phone,headers=self.headers)#获取验证码

        #获取token值
        self.api_login="/api/login"
        re = requests.post(url=self.url+self.api_login,headers=self.headers,data=json.dumps(self.data)).json()
        token = re["data"]
        self.headers["X-Access-Token"]=token

    '''def sendRequests(self,s,apiData):
        try:
            #从读取的表格中获取响应的参数作为传递
            method = apiData["method"]
            url2 = apiData["url"]
            re = s.request(method=method,url=self.url+url2,headers=self.headers,)

           # print(apiData["UseCase"],re.content.decode())
            return re
        except Exception as e:
            print(e)'''

    #切换到外场工作台
    def swith_workstation(self):
        api_out ="/api/biz/h5/work/statistics/out"
        re = requests.get(url=self.url+api_out,headers=self.headers)
        print(re.content.decode())
    #查看客户列表
    def cust_list(self):
        api="/api/biz/h5/out/customer/custList"
        re = requests.get(url=self.url + api, headers=self.headers)
        print(re.content.decode())
    #新增客户
    def add_cust(self):
        api="/api/biz/h5/out/customer/add"
        data={
            "namCustZh":"xinz",
            "codCustPhone":"14325432433",
            "codIntentionLevel":"1"
        }
        re = requests.post(url=self.url + api, headers=self.headers,data=json.dumps(data))
        print(re.content.decode())
    #置顶客户
    def top_cust(self):
        api = "/api/biz/h5/in/customer/topside/1274622495392997378"
        data={
            "codCustId": "1274622495392997378",
            "topsideStatus": "1"
        }
        re = requests.put(url=self.url + api,headers=self.headers,data=json.dumps(data))
        print(re.content.decode())

Sendrquests().top_cust()

import requests,json
class Pc():
    #基础信息
    def __init__(self):
        self.url ="https://test.guan.yatonghui.com"
        self.api ="/api/verification/code/1/"#获取验证码接口
        self.headers={
            'Eaton-Origin': 'PC',
            'Eaton-Company-CODE': 'CSGS',
            'Content-Type': 'application/json;charset=UTF-8',
            'Eaton-ORG-ID': '59613975113200000',
           }
    #登录
    def login(self):
        api="/api/login"
        data ={"username": "ceshi", "password": "12345678", "loginType": "1"}

        re = requests.post(url=self.url + api, headers=self.headers, data=json.dumps(data)).json()
        token = re["data"]
        self.headers["X-Access-Token"] = token
        print(self.headers)

    def update_positon(self):
        api =""
Pc().login()



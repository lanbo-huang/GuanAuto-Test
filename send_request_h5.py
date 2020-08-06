import requests
import json
import readxls
class SendRequests():
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

    def sendRequests(self, s, apiData):
        try:
            # 从读取的表格中获取响应的参数作为传递
            method = apiData["method"]
            url2 = apiData["url"]
            if apiData["data"] == "":
                data = None
            else:
                data = apiData["data"].encode("utf-8")
            if apiData["params"] == "":
                params = None
            else:
                params =apiData["params"]
                #print(type(data))
                #print(data)
            #print(method,self.url+url2,data)
            re = s.request(method=method, url=self.url + url2, headers=self.headers,data=data,params=params)

            # print(apiData["UseCase"],re.content.decode())
            #print(method,re.content.decode())
            return re
        except Exception as e:
            print(e)

'''if __name__ =="__main__":
    s=requests.session()
    api_datas = readxls.ReadExcel('yatong_h5.xlsx').read_data()
    n = len(api_datas)

    for i in range(n):
        api_data = api_datas[i]
        SendRequests().sendRequests(s,api_data)'''

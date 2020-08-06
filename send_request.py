import json
import sys,os
#sys.path.append(os.path.dirname(__file__))
import readxls
import requests

class SendRequests():
    def __init__(self):
        self.url="https://guan.yatonghui.com"
        self.headers={
            'Eaton-Origin': 'PC',
            'Eaton-Company-CODE': 'CSGS',
            'Content-Type':'application/json;charset=UTF-8',
            'Eaton-ORG-ID': '1206347115622981634'#对应登录账户的权限ID
        }
        self.api="/api/login"
        self.data={
            'username':'13300000110',
            'password':'123456',
            'loginType':'1'
                }
        re=requests.post(url=self.url+self.api,headers=self.headers, data=json.dumps(self.data))
        token = json.loads(re.content.decode())['data']
        self.headers["X-Access-Token"]=token #将token信息存入header
        #print(self.headers)
    def sendRequests(self,s,apiData):
        try:
            #从读取的表格中获取响应的参数作为传递
            method = apiData["method"]
            url2 = apiData["url"]
           # if apiData["data"]=="data":
             #   data=apiData["data"]
            re = s.request(method=method,url=self.url+url2,headers=self.headers,)

           # print(apiData["UseCase"],re.content.decode())
            return re
        except Exception as e:
            print(e)

'''if __name__ =="__main__":
    s=requests.session()
    api_datas = readxls.ReadExcel('yatong.xlsx').read_data()
    n = len(api_datas)

    for i in range(n):
        api_data = api_datas[i]
        SendRequests().sendRequests(s,api_data)'''








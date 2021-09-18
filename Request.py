import requests
import json
import readxls,root
import requests,json,time,datetime


class Request():
    def NewRequest(self,method,api,phone,headers,data=None,params=None,company="CSGS",port="H5"):
        #登录
        url = "https://pre.guan.yatonghui.com"
        headers =headers
        '''headers = {
            'Eaton-Origin': port,
            'Eaton-Company-CODE': company,
            'Content-Type': 'application/json;charset=UTF-8',
            'Eaton-Project-ID': '1274716042220154882' }#项目ID
        sql = "select org_id from base_employee where mobile_phone=" + phone + " and company_name ="+ "'测试公司'"
        org_id = root.get_id(sql)
        headers['Eaton-ORG-ID'] = str(org_id)'''

        api_login = "/api/login"  # 登录接口
        api_verify = "/api/verification/code/1/"  # 获取验证码接口
        data_1 = {'phone': phone, 'code': '6666', 'loginType': '6'}

        #print(data_1)

        requests.get(url=url + api_verify + phone, headers=headers)  # 获取验证码
        # 获取token值
        re = requests.post(url=url + api_login, headers=headers, data=json.dumps(data_1)).json()
        #print(re)
        token = re["data"]
        headers["X-Access-Token"] = token
        #print(headers)
        #发起请求
        #print(method, url+api, phone, data, params,headers)
        r = requests.request(method=method,headers=headers,params=params,url=url+api,data=json.dumps(data)).json()
        print(r['msg'])


    def sendRequests(self, apiData):
        try:
            # 从读取的表格中获取响应的参数作为传递
            method = apiData["method"]

            api = apiData["api"]

            phone = str(apiData["phone"]).split(".")[0]

            #print(type(phone)),print(phone)
            if apiData["data"] == "":
                data = None
            else:
                data = eval(apiData["data"])

            if apiData["params"] == "":
                params = None
            else:
                params =eval(apiData["params"])

            if apiData["headers"] == "":
                headers = None
            else:
                headers =eval(apiData["headers"])

            re = self.NewRequest(method=method,headers=headers,api=api,phone=phone,data=data,params=params)
            print(re)
            return re

        except Exception as e:
            print(e)

if __name__ =="__main__":
    s=requests.session()
    api_datas = readxls.ReadExcel('yatong_h6.xlsx').read_data()
    n = len(api_datas)


    for i in range(n):
        api_data = api_datas[i]
        #print(api_data)
        Request().sendRequests(api_data)


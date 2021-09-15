import requests,json,time,datetime,root

def Request(method,api,phone,data=None,params=None,company="CSGS",port="H5"):
    #登录
    url = "https://guan.yatonghui.com"
    headers = {
        'Eaton-Origin': port,
        'Eaton-Company-CODE': company,
        'Content-Type': 'application/json;charset=UTF-8',
        'Eaton-Project-ID': '1274716042220154882' }#项目ID
    sql = "select org_id from base_employee where mobile_phone=" + phone + " and company_name ="+ "'测试公司'"
    org_id = root.get_id(sql)
    headers['Eaton-ORG-ID'] = str(org_id)

    api_login = "/api/login"  # 登录接口
    api_verify = "/api/verification/code/1/"  # 获取验证码接口
    data_1 = {'phone': phone, 'code': '6666', 'loginType': '2'}

    requests.get(url=url + api_verify + phone, headers=headers)  # 获取验证码
    # 获取token值
    re = requests.post(url=url + api_login, headers=headers, data=json.dumps(data_1)).json()
    #print(re)
    token = re["data"]
    headers["X-Access-Token"] = token
    #发起请求
    r = requests.request(method=method,headers=headers,params=params,url=url+api,data=json.dumps(data)).json()
    print(r)

    print(r['msg'])

if __name__ =="__main__":
    api ="/api/biz/h5/out/customer/1292749237970178050"
    params = {"id":"1288011357748662273"}
    Request("get",api,"17704034087")

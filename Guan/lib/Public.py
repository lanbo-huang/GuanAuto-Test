import time,datetime,requests,json,os,sys
import configparser

requests.packages.urllib3.disable_warnings()



def Request(method,headers,api,keyword,params=None,data=None):
    '''重写request方法
    method：请求方法
    heders:通过功能方法Get_headers 获取
    api：请求接口
    keyword:请求接口的具体含义
    data：请求数据
    params：请求参数
    '''
    dir = os.path.dirname(os.path.dirname(__file__))
    cf = configparser.ConfigParser()
    cf.read(os.path.join(dir,"api","out_api.ini"),encoding="utf-8")
    url = cf.get("server","url")

    try:
        re = requests.request(method=method,headers=headers,url=url+api,params=params,data=json.dumps(data),verify=False).json()
        result = re['msg']
        res=re['data']
        if result == 'OK':
            print("{0}:请求成功".format(keyword))
        else:
            print("{0}:请求失败，请求结果{1}".format(keyword,result))
        return res
    except Exception as e:
        print(e)



def Get_headers(url,type="h5",phone="13300000024"):
    '''默认内场销售登录
       url：请求的服务器地址
       type：移动端登陆h5,PC端登陆pc，全民营销端登陆wp
    '''
    headers = {'Eaton-Company-CODE': 'CSGS',
        'Content-Type': 'application/json;charset=UTF-8'}
    global api_login,data,source
    source = "6"
    api_login = "/api/login"
    api_verfy = "/api/verification/code/1/"
    data = {'phone': phone, 'code': '6666', 'loginType': source}
    if type == "h5":
        headers["Eaton-Origin"] = "STANDARDH5"
    if type == "pc":
        headers["Eaton-Origin"] = "PC"
        source = "2"
    if type == "wp":
        headers["Eaton-Origin"] = "WHOLE"
        api_login = "/api/whole/login"  # 登录接口
        data.pop("loginType")
    try:
        # 获取验证码
        requests.get(url=url + api_verfy + phone, headers=headers,verify=False)
        # 登陆
        re = requests.post(url=url + api_login, headers=headers, data=json.dumps(data),verify=False).json()
        #获取登录令牌
        token = re["data"]
        headers["X-Access-Token"] = token


        #获取部门ID信息
        if type =="h5" or type =="pc":
            api = "/api/sys/base/employee/profile"
            org_id = requests.get(url=url + api, headers=headers, data=json.dumps(data),verify=False).json()
            headers["Eaton-ORG-ID"]= org_id["data"]["emp"]["orgId"]
        return headers

    except Exception as e:
        print("请求失败:{}".format(e))

url = "https://yapi.baidu.com/mock/20538/api/verification/code/1/13751198376"
url2 = "https://www.baidu.com"
headers = {'Eaton-Company-CODE': 'CSGS',
        'Content-Type': 'application/json;charset=UTF-8',
           'Eaton-Origin':'STANDARDH5'}
res = requests.get(url=url)
print(res)


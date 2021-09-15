#coding:utf-8
import json
import requests
requests.packages.urllib3.disable_warnings()

def send_msg(url,content):
    #钉钉发送消息
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = {
        "msgtype": "text",
        "text": { "content": content},
        "at":{"atMobiles":["13751198376"]}
    }
    r = requests.post(url,data = json.dumps(data),headers=headers)
    return r.text

if __name__ == '__main__':
    url = "https://test.guan.yatonghui.com"  # 请求域名
    url2 = 'https://oapi.dingtalk.com/robot/send?access_token=ad4e67a9b38d6d78e7432c0ef4896800e9df657c8598deb2a919a6a7e3f410b0'.format()#钉钉接口
    api = "/api/verification/code/1/"  # 获取验证码接口
    phone = "13300000014"
    headers = {
        'Eaton-Origin': 'STANDARDH5',
        'Eaton-Company-CODE': 'CSGS',
        'Content-Type': 'application/json;charset=UTF-8',
        'Eaton-ORG-ID': '1197540232292413442',
        }

    api_login = "/api/login"  # 登录接口
    data = {'phone': phone, 'code': '6666', 'loginType': '6'}
    try:
        res=requests.get(url=url + api + phone, headers=headers, verify=False).json()  # 获取验证码
        print(res)
        #获取验证码失败报警
        if res["msg"] != "OK":
            code = res['code']
            msg = res['msg']
            content = "观系统业务告警：获取验证码失败，返回code:{0},msg:{1}".format(code, msg)

            #print(send_msg(url2, content))
        else:
            #登录失败报警
            re = requests.post(url=url + api_login, headers=headers, data=json.dumps(data), verify=False).json()
            headers['X-Access-Token'] = re['data']

            if re["msg"] != "OK":
                code = re['code']
                msg = re['msg']
                content = "观系统业务告警：系统登录出现异常，返回code:{0},msg:{1}".format(code, msg)

                #print(send_msg(url2, content))
            else:
                api_employee = '/api/sys/base/employee/profile'
                result = requests.post(url=url + api_employee, headers=headers, data=json.dumps(data), verify=False).json()
                if result['status'] == "503":
                    content = "观系统业务告警：sass-sys-api没有起来，系统报错{0}".format(result['status'])
                    url2 = 'https://oapi.dingtalk.com/robot/send?access_token=ad4e67a9b38d6d78e7432c0ef4896800e9df657c8598deb2a919a6a7e3f410b0'.format()

    except Exception as error:
        content = "观系统业务告警：系统服务异常，返回错误:{0}".format(error)

       #print(send_msg(url2, content))
        print(error)







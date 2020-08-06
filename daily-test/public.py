import requests,json,time,datetime
def purchase(base_url,api,headers,data,method,type):
    with open("D:\GuanAPI-master\daily-test\guan.txt","a") as f:
        try:
            s = requests.Session()
            re = s.request(url=base_url+api,headers=headers,data=json.dumps(data),method=method).json()
            result = re['msg']
            if result == "ok":
                print(type)
                f.write(type)
                f.write("\n")
            else:
                print(result)
                f.write(result)
                f.write("\n")
        except Exception as e:
            f.write(e)
            f.write("\n")


if __name__ == "__main__":
    date = time.strftime("%Y-%m-%d")  # 日期年月日
    phone_stf = time.strftime("%Y%m%d")  # 手机号后八位的定义,用于手机号拼接及客户姓名的拼接
    assumpsitDate = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    url = "https://test.guan.yatonghui.com"
    api = "/api/verification/code/1/"  # 获取验证码接口
    headers = {
        'Eaton-Origin': 'H5',
        'Eaton-Company-CODE': 'CSGS',
        'Content-Type': 'application/json;charset=UTF-8',
        'Eaton-ORG-ID': '1197540232292413442',
        'Eaton-Project-ID': '1274716042220154882'}  # h5-onine接口报备时，必须带的头部信息，报备的项目id


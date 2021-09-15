import requests,json,time,datetime,random,root
class Purchase():
    def __init__(self):
        "基础信息"
        self.phone_stf = time.strftime("%d%H%M%S") #手机号后八位的定义,用于手机号拼接及客户姓名的拼接
        self.assumpsitDate = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S") #约看日期
        self.url ="https://test.guan.yatonghui.com" #请求域名
        self.api ="/api/verification/code/1/" #获取验证码接口
        self.purchase_prj="1274716042220154882" #报备项目ID,621项目
        self.purchase_transfer_prj="1271096380915961858" #转介的项目ID，611项目
        self.headers={
            'Eaton-Origin': 'H5',
            'Eaton-Company-CODE': 'CSGS',
            'Content-Type': 'application/json;charset=UTF-8',
            'Eaton-ORG-ID': '1197540232292413442',
            'Eaton-Project-ID': self.purchase_prj} #h5-onine接口报备时，必须带的头部信息，报备的项目id

    def login(self,phone="13300000014"):
        "默认内场销售登录"
        api_login = "/api/login"  # 登录接口
        data = {'phone': phone,'code': '6666','loginType': '2'}
        requests.get(url=self.url + self.api + phone, headers=self.headers,verify=False)  # 获取验证码
        # 获取token值
        re = requests.post(url=self.url + api_login, headers=self.headers, data=json.dumps(data),verify=False).json()
        token = re["data"]
        self.headers["X-Access-Token"] = token


    def Request(self,method,headers,url,data):
        try:
            re = requests.request(method=method,headers=headers,url=url,data=json.dumps(data),verify=False).json()
            result = re['msg']
            if result == 'OK':
                return 1
            else:
                print(result)
        except Exception as e:
            print(e)

    def OutPurchase(self):
        "外场报备流程"
        #第一步：外场报备
        type = "外场报备"
        api="/api/biz/h5/out/putrecord/add"
        prelist = ["155", "156", "157"]
        namCustZh = self.phone_stf + type
        codCustPhone = random.choice(prelist) + self.phone_stf
        data = {
            "namCustZh": namCustZh,
            "putrecordType": "1",
            "codCustPhone": codCustPhone,
            "visitCount": "2",
            "assumpsitDate": self.assumpsitDate,
            "assumpsitTime": "6",
            "codPrjId": self.purchase_prj,
            "codPrjName": "621项目",
            "codPrjCompanyId": "201900078712012912",
            "codPrjCompanyName": "万科",
            "dataList": []  }
        #登录系统
        self.headers["Eaton-ORG-ID"] = "1202262461307658241"  # 外场销售的人员的组织ID
        self.headers.pop("Eaton-Project-ID")
        self.login("13332323232")
        #报备
        result = self.Request("post", self.headers, self.url + api, data)
        # 打印报备信息
        if result == 1:
            with open("1.txt","w") as f:
                f.write("外场报备成功：客户姓名:{0},手机号:{1}".format(namCustZh, codCustPhone))

if __name__ =="__main__":
    Purchase().OutPurchase()














import requests,json,time,datetime,random,pymysql,root
class Purchase():
    def __init__(self):
        "基础信息"
        self.phone_stf = time.strftime("%Y%m%d") #手机号后八位的定义,用于手机号拼接及客户姓名的拼接
        self.assumpsitDate = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S") #约看日期
        self.url ="https://pre.guan.yatonghui.com" #请求域名
        self.api ="/api/verification/code/1/" #获取验证码接口
        self.purchase_prj="1274716042220154882" #报备项目ID,621项目
        self.purchase_transfer_prj="1271096380915961858" #转介的项目ID，611项目
        self.headers={
            'Eaton-Origin': 'H5',
            'Eaton-Company-CODE': 'CSGS',
            'Content-Type': 'application/json;charset=UTF-8',
            'Eaton-ORG-ID': '1197540232292413442',
            'Eaton-Project-ID': self.purchase_prj} #h5-onine接口报备时，必须带的头部信息，报备的项目id

    def del_data(self):
        # 1、删除报备列表产生的数据
        sql_1 = 'delete from cust_putrecord where corp_name="测试公司"  and cod_cust_phone like"' + '%' + self.phone_stf + '"'
        root.delete_data(sql_1)
        # 2、删除内场客户
        sql_2 = "delete from cust_info where  corp_id='201900078712012912' and cod_cust_phone like '%" + self.phone_stf + "'"
        root.delete_data(sql_2)
        # 3、删除外场客户
        sql_3 = "delete from rea_customer_info where  corp_id='201900078712012912' and cod_cust_phone like '%" + self.phone_stf + "'"
        root.delete_data(sql_3)
        # 4、删除全民客户
        sql_4 = "delete from whole_customer where  company_id='201900078712012912' and phone like '%" + self.phone_stf + "'"
        root.delete_data(sql_4)

    def login(self,phone="13300000014"):
        "默认内场销售登录"
        api_login = "/api/login"  # 登录接口
        data = {'phone': phone,'code': '6666','loginType': '2'}
        requests.get(url=self.url + self.api + phone, headers=self.headers)  # 获取验证码
        # 获取token值
        re = requests.post(url=self.url + api_login, headers=self.headers, data=json.dumps(data)).json()
        token = re["data"]
        self.headers["X-Access-Token"] = token

    def login_wp(self,phone="19400000014"):
        api_login = "/api/whole/login"  # 登录接口
        data = { 'phone': phone,'code': '6666'}
        requests.get(url=self.url + self.api + phone, headers=self.headers)  # 获取验证码
        # 获取token值
        re = requests.post(url=self.url + api_login, headers=self.headers, data=json.dumps(data)).json()
        token = re["data"]
        self.headers["X-Access-Token"] = token

    def Request(self,method,headers,url,data):
        try:
            re = requests.request(method=method,headers=headers,url=url,data=json.dumps(data)).json()
            result = re['msg']
            if result == 'OK':
                return 1
            else:
                print(result)
        except Exception as e:
            print(e)


    def NaturalPurchase(self):
        "自然来访报备流程"
        #第一步：新增报备
        type ="自然来访"
        prelist = ["136","137","138","139","147","150"]
        namCustZh = self.phone_stf+type #报备客户姓名：日期+自然来访
        codCustPhone = random.choice(prelist)+self.phone_stf #报备客户电话：当天的年月日结尾
        codPrjId = self.purchase_prj #报备项目：621项目的prjid
        #报备数据
        custPutrecordList={"namCustZh":namCustZh,"codCustPhone":codCustPhone,"visitCount":"2","oneselfVisit":"1"}
        list=[custPutrecordList]
        api = "/api/biz/h5/online/in/putrecord/add"  # 报备接口
        data ={"codPrjId":codPrjId,"custPutrecordList":list}
        #报备
        self.login()
        result = self.Request("post",self.headers,self.url+api,data)
        #打印报备信息
        if result == 1:
            print("自然来访报备流程开始")
            print("1、报备成功  客户姓名:{0},手机号:{1}".format(namCustZh,codCustPhone))

        #第二步：确认到访
        #1、获取报备ID
        sql = "SELECT id FROM `cust_putrecord` where cod_cust_phone='" + codCustPhone + "'"
        id = root.get_id(sql)
        #2、确认到访
        api = "/api/biz/h5/in/putrecord/beginReceiveCust"  # 确认到访接口
        data = {"putrecordId": id, "putrecordStatus": "7"}
        result = self.Request("put", self.headers, self.url + api, data)
        #打印到访信息
        if result == 1:
            print("2、到访成功")

        #第三步：完成接待
        api = "/api/biz/h5/in/putrecord/endReceiveCust"  # 完成接待接口
        data = {"putrecordId": id, "putrecordStatus": "18"}
        result = self.Request("put", self.headers, self.url + api, data)
        # 打印接待信息
        if result == 1:
            print("3、完成接待")

    def TokerPurchase(self):
        "自行拓客报备流程"
        #第一步：新增客户
        api="/api/biz/h5/in/customer/add"
        type ="自行拓客"
        prelist=["130","131","132","133","134","135"]
        namCustZh = self.phone_stf+type
        codCustPhone = random.choice(prelist)+ self.phone_stf
        #数据信息
        custInfo = {"namCustZh": namCustZh,"codCustPhone": codCustPhone, "codIntentionLevel": "1","oneselfVisit": "4","phoneCanEdit": "true" }
        data ={"custInfo": custInfo,"dataList": []}
        #新增客户
        self.login()
        result = self.Request("post", self.headers, self.url + api, data)
        #打印客户信息
        if result == 1:
            print("自行拓客报备流程开始")
            print("1、新增客户成功  客户姓名:{0},手机号:{1}".format(namCustZh, codCustPhone))

        #第二步，报备客户
        # 1、查询到新增客户的id号
        sql = "select id from cust_info where  corp_id='201900078712012912' and cod_cust_phone like '%" + self.phone_stf + "'"
        id = root.get_id(sql)
        #报备接口
        api = "/api/biz/h5/in/putrecord/addPutrecord"
        data = {
            "rjName": "621项目",
            "currentPrjId": self.purchase_prj,
            "namCustZh": namCustZh,
            "codCustPhone": codCustPhone,
            "codCustId": id,
            "oneselfVisit": "4",
            "codPrjId": self.purchase_prj,
            "assumpsitDate": self.assumpsitDate,
            "assumpsitTime": "11",
            "assign": "0",
            "visitCount": "2"}
        result = self.Request("post", self.headers, self.url + api, data)
        # 打印报备信息
        if result == 1:
            print("2、报备成功")

        # 第三步，确认到访
        # 获取报备客户的报备ID 号
        sql = "SELECT id FROM `cust_putrecord` where cod_cust_phone='" + codCustPhone + "'"
        id_2 = root.get_id(sql)
        api = "/api/biz/h5/in/putrecord/toRegister"
        data = {"putrecordStatus": "3","putrecordId": id_2}
        # 打印到访信息
        if result == 1:
            print("3、确认到访")

    def TransferPurchase(self):
        '''内场销售-内场转介流程'''
        # 第一步：新增客户
        api = "/api/biz/h5/in/customer/add"
        type = "内场转介"
        prelist = ["151","152","153","155","156","157","158","159","186","187","188"]
        namCustZh = self.phone_stf + type
        codCustPhone = random.choice(prelist) + self.phone_stf
        custInfo = {
            "namCustZh": namCustZh,
            "codCustPhone": codCustPhone,
            "codIntentionLevel": "1",
            "oneselfVisit": "4",
            "phoneCanEdit": "true"}
        data = {"custInfo": custInfo,"dataList": []
        }
        #新增客户
        self.login()
        result = self.Request("post", self.headers, self.url + api, data)
        # 打印客户信息
        if result == 1:
            print("内场转介报备流程开始")
            print("1、新增客户成功  客户姓名:{0},手机号:{1}".format(namCustZh, codCustPhone))

        #第二步：内场转介报备客户
        # 查询到新增客户的id号
        sql = "select id from cust_info where  corp_id='201900078712012912' and cod_cust_phone like '%" + self.phone_stf + "'"
        id = root.get_id(sql)
        # 报备客户
        api = "/api/biz/h5/in/putrecord/addPutrecord"
        data = {
	            "namPrjName": "0611",
	            "namCustZh": namCustZh,
	            "codCustPhone": codCustPhone,
	            "codCustId": id,
	            "oneselfVisit": "3",
	            "codPrjId": self.purchase_transfer_prj,
	            "assumpsitDate": self.assumpsitDate,
	            "assumpsitTime": "0",
	            "assign": 0,
	            "visitCount": "2"}
        result = self.Request("post", self.headers, self.url + api, data)
        # 打印报备信息
        if result == 1:
            print("2、报备成功")

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
            print("外场报备流程开始")
            print("1、报备成功  客户姓名:{0},手机号:{1}".format(namCustZh, codCustPhone))

        #第二步：确认到访
        api="/api/biz/h5/out/putrecord/toRegister"
        #获取报备ID
        sql = "SELECT id FROM `cust_putrecord` where cod_cust_phone='" + codCustPhone + "'"
        id_2 = root.get_id(sql)
        data ={"putrecordStatus":"3","putrecordId":id_2}
        result = self.Request("post", self.headers, self.url + api, data)
        # 打印报备信息
        if result == 1:
            print("2、确认到访")

    def ChannelPurchase(self):
        """渠道报备流程"""
        # 第一步：报备客户
        type = "渠道报备"
        api = "/api/biz/h5/out/putrecord/add"
        prelist = ["158", "159", "186"]
        namCustZh = self.phone_stf + type
        codCustPhone = random.choice(prelist) + self.phone_stf
        data = {
	        "assumpsitDate": self.assumpsitDate,
	        "assumpsitTime": "0",
	        "codCustPhone": codCustPhone,
	        "codPrjCompanyId": "201900078712012912",
	        "codPrjCompanyName": "万科",
            "codPrjId": self.purchase_prj,
            "codPrjName": "621项目",
            "namCustZh": namCustZh,
            "putrecordType": "1",
            "visitCount": "2"}
        # 登录系统
        self.headers["Eaton-ORG-ID"] = "1271108597354143745"  # 外部合作公司的组织ID
        self.headers.pop("Eaton-Project-ID")
        self.login("13300000126")
        #报备
        result = self.Request("post", self.headers, self.url + api, data)
        # 打印报备信息
        if result == 1:
            print("渠道报备流程开始")
            print("1、报备成功  客户姓名:{0},手机号:{1}".format(namCustZh, codCustPhone))

        #第二步：确认到访
        api = "/api/biz/h5/out/putrecord/toRegister"
        #获取报备ID
        sql = "SELECT id FROM `cust_putrecord` where cod_cust_phone='" + codCustPhone + "'"
        id_2 = root.get_id(sql)

        data = {"putrecordStatus": "3", "putrecordId": id_2}
        result = self.Request("post", self.headers, self.url + api, data)
        # 打印到访信息
        if result == 1:
            print("2、确认到访")

    def WpPurchase(self):
        "全民营销报备路程"
        self.headers.pop("Eaton-Project-ID")
        self.headers["Eaton-Origin"] = "WHOLE"
        self.api ="/api/verification/code2/1/"

        #推荐用户
        type ="全民营销"
        api="/api/biz/h5/whole/put/record"
        prelist = [ "187", "188"]
        namCustZh = self.phone_stf + type
        codCustPhone = random.choice(prelist) + self.phone_stf
        data = {
            "codPrjId": self.purchase_prj,
            "assumpsitDate": self.assumpsitDate,
            "assumpsitTime": "7",
            "visitCount": "2",
            #"putrecordDesc": "",
            "codCustPhone": codCustPhone,
            "namCustZh":namCustZh}

        # 登录系统
        self.login_wp()
        result = self.Request("post", self.headers, self.url + api, data)
        # 打印报备信息
        if result == 1:
            print("全民营销报备流程开始")
            print("1、报备成功  客户姓名:{0},手机号:{1}".format(namCustZh, codCustPhone))

if __name__ =="__main__":
    Purchase().del_data()
    Purchase().NaturalPurchase()
    Purchase().TokerPurchase()
    Purchase().TransferPurchase()
    Purchase().OutPurchase()
    Purchase().ChannelPurchase()
    Purchase().WpPurchase()













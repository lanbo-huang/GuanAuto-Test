import requests,json,time,datetime,random,pymysql,root
class Purchase():
    #基础信息
    def __init__(self):
        self.date = time.strftime("%Y-%m-%d")#日期年月日
        self.phone_stf = time.strftime("%Y%m%d")#手机号后八位的定义,用于手机号拼接及客户姓名的拼接
        self.assumpsitDate = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.url ="https://guan.yatonghui.com"
        self.api ="/api/verification/code/1/"#获取验证码接口
        self.headers={
            'Eaton-Origin': 'H5',
            'Eaton-Company-CODE': 'CSGS',
            'Content-Type': 'application/json;charset=UTF-8',
            'Eaton-ORG-ID': '1197540232292413442',
            'Eaton-Project-ID': '1274716042220154882'}#h5-onine接口报备时，必须带的头部信息，报备的项目id
        #self.phone="13300000014"#登录账号
    def del_data(self):
        # 1、删除报备列表产生的数据
        sql_1 = 'delete from cust_putrecord where corp_name="测试公司" and update_time like' + '"' + self.date + '%' + '"' + ' and cod_cust_phone like"' + '%' + self.phone_stf + '"'
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
        data = {'phone': phone,'code': '6666','loginType': '2'}
        requests.get(url=self.url + self.api + phone, headers=self.headers)  # 获取验证码
        # 获取token值
        api_login = "/api/login"#登录接口
        re = requests.post(url=self.url + api_login, headers=self.headers, data=json.dumps(data)).json()
        token = re["data"]
        self.headers["X-Access-Token"] = token
    def login_wp(self):
        data = { 'phone': self.phone,'code': '6666'}
        requests.get(url=self.url + self.api + self.phone, headers=self.headers)  # 获取验证码
        # 获取token值
        api_login = "/api/whole/login"  # 登录接口
        re = requests.post(url=self.url + api_login, headers=self.headers, data=json.dumps(data)).json()
        token = re["data"]
        self.headers["X-Access-Token"] = token

    def Natural_purchase(self):
        '''
        内场销售-自然来访报备流程
        '''
        #第一步：新增报备-自然来访
        type="自然来访"
        date = time.strftime("%Y%m%d")
        prelist=["136","137","138","139","147","150"]

        namCustZh=date+type#报备客户姓名：日期+自然来访
        codCustPhone=random.choice(prelist)+date#报备客户电话：当天的年月日结尾
        visitCount="2"
        codPrjId="1274716042220154882"#报备项目：621项目的prjid
        oneselfVisit="1"
        custPutrecordList={
            "namCustZh":namCustZh,
            "codCustPhone":codCustPhone,
            "visitCount":visitCount,
            "oneselfVisit":oneselfVisit,

        }
        list=[custPutrecordList]
        data ={
            "codPrjId":codPrjId,
            "custPutrecordList":list

        }
        api="/api/biz/h5/online/in/putrecord/add"#报备接口
        self.login()
        try:
            re = requests.post(url=self.url + api, headers=self.headers, data=json.dumps(data)).json()
            result = re['msg']
            if result=='OK':#判断是否报备成功
                print("内场销售-自然来访报备流程开始")
                print('1、报备成功')
            else:
                print(result)
        except Exception as e:
            print(e)

        #同一个用户二次报备
        #
        #第二步：确认到访
        #1、获取报备客户的报备ID 号
        sql="SELECT id FROM `cust_putrecord` where cod_cust_phone='"+codCustPhone+"'"
        #print(sql)
        id = root.get_id(sql)
        #print(id)
        #print(codCustPhone)
        #2、确认到访
        api="/api/biz/h5/in/putrecord/beginReceiveCust"#确认到访接口
        data={
            "putrecordId":id,
            "putrecordStatus":"7"
        }

        try:
            re = requests.put(url=self.url + api, headers=self.headers, data=json.dumps(data)).json()
            result = re['msg']
            if result=='OK':#判断是否确认到访成功
                print('2、确认到访成功')
            else:
                print(result)
        except Exception as e:
            print(e)
        #第三步：完成接待
        api="/api/biz/h5/in/putrecord/endReceiveCust"#完成接待接口
        data={
            "putrecordId":id,
            "putrecordStatus":"18"
        }

        try:
            re = requests.put(url=self.url + api, headers=self.headers, data=json.dumps(data)).json()
            result = re['msg']
            if result=='OK':#判断是否完成接待
                print('3、完成接待')
            else:
                print(result)
        except Exception as e:
            print(e)
    def Toker_purchase(self):
        '''
        内场销售-自行拓客报备流程开始
        :return:
        '''
        #第一步：新增客户
        api="/api/biz/h5/in/customer/add"
        type ="自行拓客"
        prelist=["130","131","132","133","134","135"]
        namCustZh = self.phone_stf+type
        codCustPhone = random.choice(prelist)+ self.phone_stf
        custInfo = {
            "namCustZh": namCustZh,
            "codCustPhone": codCustPhone,
            "contactNumberOneFlag": "n",
            "contactNumberTwoFlag": "n",
            "codIntentionLevel": "1",
            "oneselfVisit": "4",
            "phoneCanEdit": "true"
        }
        list= {
		    "fieldCode": "sex",
		    "fieldName": "性别",
		    "fieldDataType": "1",
		    "fieldLable": "基础信息",
		    "fieldDispyType": "4",
		    "fieldNotEmpty": "0",
		    "parentCode": "-1",
		    "prop": "sex_1",
		    "fieldRequired": "false"}
        data ={
            "custInfo": custInfo,
            "dataList": [list]
        }
        #print(data)
        self.login()
        try:
            re = requests.post(url=self.url + api, headers=self.headers, data=json.dumps(data)).json()
            result = re['msg']
            if result == 'OK':  # 判断是否完成接待
                print('内场销售-自行拓客报备流程开始')
                print("1、新增客户成功")
            else:
                print(result)
        except Exception as e:
            print(e)

        #第二步，报备客户
        #1、查询到新增客户的id号
        sql="select id from cust_info where  corp_id='201900078712012912' and cod_cust_phone like '%"+self.phone_stf+"'"
        id = root.get_id(sql)
        api ="/api/biz/h5/in/putrecord/addPutrecord"
        data = {
            "rjName": "621项目",
            "currentPrjId": "1274716042220154882",
            "namCustZh": namCustZh,
            "codCustPhone": codCustPhone,
            "codCustId": id,
            "oneselfVisit": "4",
            "codPrjId": "1274716042220154882",
            "assumpsitDate": self.assumpsitDate,
            "assumpsitTime": "11",
            "assign": "0",
            "visitCount": "2"
        }

        try:
            re = requests.post(url=self.url + api, headers=self.headers, data=json.dumps(data)).json()
            result = re['msg']
            if result == 'OK':  # 判断是否完成接待
                print("2、报备成功")
            else:
                print(re["code"],result)
        except Exception as e:
            print(e)

        #第三步，确认到访
        # 1、获取报备客户的报备ID 号
        sql = "SELECT id FROM `cust_putrecord` where cod_cust_phone='" + codCustPhone + "'"
        id_2 = root.get_id(sql)
        api="/api/biz/h5/in/putrecord/toRegister"
        data ={
            "putrecordStatus": "3",
            "putrecordId": id_2
        }
        try:
            re = requests.post(url=self.url + api, headers=self.headers, data=json.dumps(data)).json()
            result = re['msg']
            if result == 'OK':  # 判断是否完成接待
                print("3、确认到访成功")
            else:
                print(re["code"], result)
        except Exception as e:
            print(e)
    def Transfer_purchase(self):
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
            "contactNumberOneFlag": "n",
            "contactNumberTwoFlag": "n",
            "codIntentionLevel": "1",
            "oneselfVisit": "4",
            "phoneCanEdit": "true"
        }
        list = {
            "fieldCode": "sex",
            "fieldName": "性别",
            "fieldDataType": "1",
            "fieldLable": "基础信息",
            "fieldDispyType": "4",
            "fieldNotEmpty": "0",
            "parentCode": "-1",
            "prop": "sex_1",
            "fieldRequired": "false"}
        data = {
            "custInfo": custInfo,
            "dataList": [list]
        }
        # print(data)
        self.login()
        try:
            re = requests.post(url=self.url + api, headers=self.headers, data=json.dumps(data)).json()
            result = re['msg']
            if result == 'OK':  # 判断是否完成接待
                print('内场销售-内场转介流程开始')
                print("1、新增客户成功")
            else:
                print(result)
        except Exception as e:
            print(e)

        #第三步：报备客户
        # 1、查询到新增客户的id号
        sql = "select id from cust_info where  corp_id='201900078712012912' and cod_cust_phone like '%" + self.phone_stf + "'"
        id = root.get_id(sql)
        api = "/api/biz/h5/in/putrecord/addPutrecord"
        data = {
	            "namPrjName": "0611",
	            "namCustZh": namCustZh,
	            "codCustPhone": codCustPhone,
	            "codCustId": id,
	            "oneselfVisit": "3",
	            "codPrjId": "1271096380915961858",
	            "assumpsitDate": self.assumpsitDate,
	            "assumpsitTime": "0",
	            "assign": 0,
	            "visitCount": "2"}
        try:
            re = requests.post(url=self.url + api, headers=self.headers, data=json.dumps(data)).json()
            result = re['msg']
            if result == 'OK':  # 判断是否完成接待
                print("2、报备成功")
            else:
                print(re["code"],result)
        except Exception as e:
            print(e)
    def Out_purchase(self):
        """
        外销销售（内部）-外场报备流程
        :return:
        """
        self.headers["Eaton-ORG-ID"] ="1202262461307658241"
        self.headers.pop("Eaton-Project-ID")
        #self.phone ="13332323232"

        #第二步：报备客户
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
            "codPrjId": "1274716042220154882",
            "codPrjName": "621项目",
            "codPrjCompanyId": "201900078712012912",
            "codPrjCompanyName": "万科",
            "dataList": []
        }
        #登录系统
        self.login("13332323232")
        try:
            re = requests.post(url=self.url + api, headers=self.headers, data=json.dumps(data)).json()
            result = re['msg']
            if result == 'OK':  # 判断是否完成接待
                print("内场销售的外场报备流程开始")
                print("1、报备成功")
            else:
                print(re["code"],result)
        except Exception as e:
            print(e)

        #确认到访
        api="/api/biz/h5/out/putrecord/toRegister"
        sql = "SELECT id FROM `cust_putrecord` where cod_cust_phone='" + codCustPhone + "'"
        id_2 = root.get_id(sql)
        data ={"putrecordStatus":"3","putrecordId":id_2}
        try:
            re = requests.post(url=self.url + api, headers=self.headers, data=json.dumps(data)).json()
            result = re['msg']
            if result == 'OK':
                print("2、确认到访成功")
            else:
                print(re["code"],result)
        except Exception as e:
            print(e)

    def Channel_purchase(self):
        """外部合作公司-渠道报备流程"""
        self.headers["Eaton-ORG-ID"] = "1271108597354143745"
        self.headers.pop("Eaton-Project-ID")
        #self.phone = "13300000126"

        # 第二步：报备客户
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
            "codPrjId": "1274716042220154882",
            "codPrjName": "621项目",
            "namCustZh": namCustZh,
            "putrecordType": "1",
            "visitCount": "2"}
        # 登录系统
        self.login("13300000126")
        try:
            re = requests.post(url=self.url + api, headers=self.headers, data=json.dumps(data)).json()
            result = re['msg']
            if result == 'OK':  # 判断是否完成接待
                print("外部合作公司的外场报备流程开始")
                print("1、报备成功")
            else:
                print(re["code"], result)
        except Exception as e:
            print(e)

        # 确认到访
        api = "/api/biz/h5/out/putrecord/toRegister"
        sql = "SELECT id FROM `cust_putrecord` where cod_cust_phone='" + codCustPhone + "'"
        id_2 = root.get_id(sql)
        data = {"putrecordStatus": "3", "putrecordId": id_2}
        try:
            re = requests.post(url=self.url + api, headers=self.headers, data=json.dumps(data)).json()
            result = re['msg']
            if result == 'OK':
                print("2、确认到访成功")
            else:
                print(re["code"], result)
        except Exception as e:
            print(e)

    def Wp_purchase(self):
        """
        全民营销报备流程
        :return:
        """
        self.headers.pop("Eaton-Project-ID")
        self.headers["Eaton-Origin"] = "WHOLE"
        self.phone = "19400000014"
        self.api ="/api/verification/code2/1/"

        #推荐用户
        type ="全民营销"
        api="/api/biz/h5/whole/put/record"
        prelist = [ "187", "188"]
        namCustZh = self.phone_stf + type
        codCustPhone = random.choice(prelist) + self.phone_stf
        data = {
            "codPrjId": "1274716042220154882",
            "assumpsitDate": self.assumpsitDate,
            "assumpsitTime": "7",
            "visitCount": "2",
            "putrecordDesc": "",
            "codCustPhone": codCustPhone,
            "namCustZh":namCustZh,
            "inSalesId": "",
            "inSalesPhone": "",
            "inSalesName": "请选择内场接待员",
            "inSalesDeptId": ""}
        # 登录系统
        self.login_wp()
        try:
            re = requests.post(url=self.url + api, headers=self.headers, data=json.dumps(data)).json()
            result = re['msg']
            if result == 'OK':  # 判断是否完成接待
                print("全民营销报备流程开始")
                print("1、报备成功")
            else:
                print(re["code"], result)
        except Exception as e:
            print(e)






if __name__ =="__main__":
    #Purchase().del_data()
    Purchase().Natural_purchase()
    Purchase().Toker_purchase()
    Purchase().Transfer_purchase()
    Purchase().Out_purchase()
    Purchase().Channel_purchase()
    Purchase().Wp_purchase()










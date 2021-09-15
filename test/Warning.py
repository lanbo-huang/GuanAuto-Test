#coding:utf-8
import json
import requests
import time,pymysql
requests.packages.urllib3.disable_warnings()

class Warnnig():
    """
    1、监测url：init方法中修改
    2、监测项目 ：init方法中查看
    3、数据库变更：mysql_connect方法中修改
    4、监测公司：init方法中修改
    """
    def __init__(self):
        #钉钉robot
        self.robot_url = "https://oapi.dingtalk.com/robot/send?access_token=ad4e67a9b38d6d78e7432c0ef4896800e9df657c8598deb2a919a6a7e3f410b0"
        # 请求域名
        self.url = "https://guan.yatonghui.com"
        # 项目ID,现网WY，心跳监测项目
        self.prj_id = "1334696151703580674"
        # 验证码接口
        self.verify_api = "/api/verification/code/1/"
        #请求头
        self.headers = {
            'Eaton-Company-CODE': 'WY',
            'Content-Type': 'application/json;charset=UTF-8',
            'Eaton-Origin': 'STANDARDH5'
        }

    def mysql_connect(self):
        # 1、测试环境数据库
        #conn = pymysql.connect(host='rm-wz98ju5jwvu87p8l86o.mysql.rds.aliyuncs.com', user="local_develop",password="Ytonghui&!local110", database="guan_qc", charset="utf8")
        #2、生产环境数据库
        conn = pymysql.connect(host='rm-wz96xqxw14qo6edaxio.mysql.rds.aliyuncs.com', user="hwy",password="HWY@112233", database="guan_prod", charset="utf8")
        return conn

    def get_custid(self,sql):
        conn = self.mysql_connect()
        curson = conn.cursor()
        try:
            curson.execute(sql)
            id = curson.fetchone()[0]
            conn.close()
            return id
        except Exception as e:
            print(e)

    def send_msg(self,content):
        #钉钉发送消息
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        data = {
            "msgtype": "text",
            "text": { "content": content},
            "at":{"atMobiles":["13751198376"]}
        }
        r = requests.post(self.robot_url,data = json.dumps(data),headers=headers)
        return r.text

    def verification_code(self,phone="19000000003"):
        '''
        默认内场销售19000000003，获取验证码失败告警
        uc\gateway 服务出现异常告警
        '''
        warning="no"
        try:
            res = requests.get(url=self.url + self.verify_api + phone, headers=self.headers, verify=False).json()
            if res["code"] == 500:
                warning="yes"
                content = "观系统业务告警：系统uc服务出现异常,返回code：{0}，msg：{1}".format(res["code"],res["msg"])
                self.send_msg(content)

        except Exception as error:
            warning="yes"
            content = "观系统业务告警：系统gateway服务出现异常，返回{}".format(error)
            self.send_msg(content)
        finally:
            return warning

    def get_headers(self,type="h5", phone="19000000003"):
        '''
        默认内场销售登录
        url：请求的服务器地址
        type：移动端登陆h5,PC端登陆pc，全民营销端登陆wp
        sys服务告警及登录告警
        '''
        warning = "no"
        headers = {
            'Eaton-Company-CODE': 'WY',
            'Content-Type': 'application/json;charset=UTF-8',
        }
        global api_login, data, source
        source = "6"
        api_login = "/api/login"
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
            requests.get(url=self.url + self.verify_api + phone, headers=headers, verify=False)
            # 登陆
            re = requests.post(url=self.url + api_login, headers=headers, data=json.dumps(data), verify=False).json()
            if re["code"] == 0:
                # 获取登录令牌
                token = re["data"]
                headers["X-Access-Token"] = token

                # 获取部门ID信息
                if type == "h5" or type == "pc":
                    api = "/api/sys/base/employee/profile"
                    org_id = requests.get(url=self.url + api, headers=headers, data=json.dumps(data), verify=False).json()
                    #print(org_id)

                    if org_id["code"]== 0:
                        headers["Eaton-ORG-ID"] = org_id["data"]["emp"]["orgId"]

            else:
                warning="yes"
                content = "观系统业务告警：登录出现异常，返回{}".format(re["msg"])
                self.send_msg(content)


        except Exception as e:
            warning="yes"
            content = "观系统业务告警：saas-sys-api服务出现异常".format(e)
            self.send_msg(content)

        finally:
            return [headers,warning]

    def get_ideamark(self,code):
        """
        获取包含ideamark的请求头
        biz服务异常告警
        code:新增客户是为cust，报备时为putrecord
        """
        api = "/api/biz/ide/mark/createIdeMark"
        ideamark_headers = self.get_headers()[0]
        params = {"code":code}
        warning = "no"
        list = []
        #print(res["status"])
        try:
            res = requests.get(url=self.url + api, headers=ideamark_headers, params=params, verify=False).json()

            if res["code"] ==0:
                ideamark_headers["idea-mark"] = res["data"]

            else:
                warning="yes"
                content = "观系统业务告警：获取ideamark失败，类型{0}".format(code)
                self.send_msg(content)

        except Exception as e:
            warning = "yes"
            content = "观系统业务告警：sass-biz-api服务出现异常，返回{0}".format(e)
            self.send_msg(content)
        finally:
            return [ideamark_headers,warning]

    def add_cust(self):
        #内场新增客户
        headers = self.get_ideamark("cust")[0]
        headers["Eaton-Project-ID"] = self.prj_id
        codCustPhone = "199"+time.strftime("%d%H%M%S")
        id = "null"
        #print(codCustPhone)
        warning = "no"
        api="/api/biz/h5/in/customer/add"
        data = { "custInfo": {"namCustZh": "内场" + time.strftime("%m%d%H%M%S"),"codCustPhone": codCustPhone,
		        "codIntentionLevel": "0","oneselfVisit": "4", },
		        "dataList": [] }

        try:
            res = requests.post(url=self.url+api,headers=headers,data=json.dumps(data),verify=False).json()
            if res["code"] == 0:
                sql = "select id from cust_info where cod_cust_phone =" + "'" + codCustPhone + "'"
                id = self.get_custid(sql)
               # print(sql)
               # print(id)
            else:
                warning ="yes"
        except Exception as error:
            warning = "yes"
        finally:
            return[id,warning]

    def workflow_warnling(self):
        api = "/api/biz/h5/in/customer/follow/add"
        cust_id = self.add_cust()[0]
        #print(cust_id)
        data ={"custIntentId": cust_id, "codCustState": "02", "codIntentionLevel": "0",
         "easCusFollow": {"custIntentId": cust_id, "codCustState": "02", "codIntentionLevel": "0",
                          "followAway": "0", "followRemarks": "1"}, "dataList": []}
        try:
            headers = self.get_headers()[0]

            headers["Eaton-Project-ID"] = self.prj_id
            res = requests.post(url=self.url + api, headers=headers, data=json.dumps(data), verify=False).json()
            #print(res)

            if res["code"] == 500:
                content="观系统业务告警：工作流服务出现异常，返回code：{0}, msg：{1}".format(res["code"],res["msg"])
                self.send_msg(content)
        except Exception as e:
            content = "观系统业务告警：工作流服务出现异常，返回原因{}".format(e)
            self.send_msg(content)


if __name__ == "__main__":
    W = Warnnig()
    if W.verification_code() == "no": #uc\gataway不告警
        if W.get_headers()[1] == "no":#登录\sys不告警
            if W.get_ideamark("cust")[1] == "no":#biz不告警----------
                if W.add_cust()[1] == "no":#新增客户不失败
                   W.workflow_warnling()#工作流是正常






























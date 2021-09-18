__author__ = "hwy"
import configparser as cfparser
import requests,json,os
from jsonpath_rw import parse



class GetToken():
    def __init__(self,corpcode="CSGS"):
        """
        :param corpcode: 公司的code，默认CSGS
        """
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.cf = cfparser.ConfigParser()
        self.cf.read(self.parent_dir+"/config/config.ini",encoding="utf-8")
        self.environment = self.cf.get("environment","environment")
        self.corpcode = corpcode
        self.url = "https://" + self.environment + ".guan.yatonghui.com"



    def get_token(self,login_type,phone):
        """
        登录形式login_type : h5或者pc
        主要作用：获取带token值的header
        """
        if login_type =="h5":
            eaton_origin = self.cf.get("h5", "Eaton-Origin")
            login_Type = self.cf.get("h5", "loginType")
        else:
            eaton_origin = self.cf.get("pc", "Eaton-Origin")
            login_Type = self.cf.get("pc", "loginType")

        headers = {"Eaton-Company-CODE": self.corpcode, "Eaton-Origin": eaton_origin,'Content-Type': 'application/json;charset=UTF-8'}
        data = {"code": "6666", "loginType": login_Type, "phone": phone}

        verif_code_api = "/api/verification/code/1/"
        login_api = "/api/login"

        #获取验证码
        requests.get(self.url+verif_code_api+phone,headers=headers).json()
        #登录
        res = requests.post(self.url+login_api,headers=headers,data=json.dumps(data)).json()
        #获取token值，用jsonpath_rw的parse去匹配结果，返回来的是list，所以用切片的形式取回来
        X_Access_Token = [i.value for i in (parse("data")).find(res)][0]
        #把token带入headers中
        headers["X-Access-Token"]=X_Access_Token
        #返回header值
        return headers


    def get_orgid_headers(self,login_type,phone):
        '''
        返回带orgid的header
        '''
        headers = self.get_token(login_type,phone)
        api = "/api/sys/base/employee/profile"
        paramas = {"orgId":""}
        res = requests.get(url= self.url+ api,headers=headers,params=json.dumps(paramas)).json()

        eaton_org_id = [i.value for i in (parse("data.emp[*].orgId")).find(res)][0]
        headers["Eaton-ORG-ID"] = eaton_org_id
        return headers



    def get_projectid_headers(self,login_type,phone):
        """
        返回带project-id的全量headers,只有内场的H5才会用到
        :param login_type:
        :return:
        """
        api = "/api/biz/h5/in/project/my/select"
        paramas = {"onlineStatus":"1" }
        headers = self.get_orgid_headers(login_type,phone)
        res = requests.get(url=self.url + api, headers=headers, params=json.dumps(paramas)).json()
        eaton_project_id = [i.value for i in (parse("data.defaultPrj")).find(res)][0]

        if eaton_project_id == None:
            headers["Eaton-Project-ID"] = ""
        else:
            headers["Eaton-Project-ID"] = eaton_project_id
        return headers

    def get_idea_mark_headers(self,headers,mark_type=None):
        """
        获取带idea_mark的头部信息
        :param mark_type: employee--新增员工，cust---新增客户
        :return:
        """
        api = "/api/biz/ide/mark/createIdeMark"
        paramas = {"code":mark_type}
        res = requests.get(url=self.url + api, headers=headers, params=json.dumps(paramas)).json()
        idea_mark = [i.value for i in (parse("data")).find(res)][0]
        headers["idea-mark"] = idea_mark
        return headers





if __name__ == "__main__":
    corpcode = "WK"
    gettoken = GetToken(corpcode=corpcode)
    gettoken.get_token('pc',"15200001111")



import requests,json,os
from jsonpath_rw import  parse
from requests_toolbelt.utils import dump



class SendRequests():
    """
    默认登录发起请求，
    """
    def __init__(self,environment,code,phone):
        self.url ="https://"+environment+".guan.yatonghui.com"
        #self.header = {"Eaton-Company-CODE":"MCGS", "Eaton-Origin": "STANDARDH5",'Content-Type': 'application/json;charset=UTF-8'}
        self.phone = phone
        self.code = code

    def get_token(self,login_type,phone):
        """
        登录形式login_type : h5或者pc
        主要作用：获取带token值的header
        """
        if login_type =="h5":
            eaton_origin ="STANDARDH5"
            login_Type = "6"
        else:
            eaton_origin ="PC"
            login_Type = "2"

        headers = {"Eaton-Company-CODE":self.code, "Eaton-Origin": eaton_origin,'Content-Type': 'application/json;charset=UTF-8'}
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

    def get_idea_mark_headers(self,login_type,phone,mark_type=None):
        """
        获取带idea_mark的头部信息
        :param mark_type: employee--新增员工，cust---新增客户
        :return:
        """
        api = "/api/biz/ide/mark/createIdeMark"
        paramas = {"code":mark_type}
        headers = self.get_projectid_headers(login_type,phone)
        res = requests.get(url=self.url + api, headers=headers, params=json.dumps(paramas)).json()
        idea_mark = [i.value for i in (parse("data")).find(res)][0]
        headers["idea-mark"] = idea_mark
        return headers


    def sendRequests(self, s, apiData):
        #这个方法目前没用了
        try:
            # 从读取的表格中获取响应的参数作为传递
            method = apiData["method"]
            api = apiData["url"]

            if apiData["data"] == "":
                data = None
            else:
                data = apiData["data"].encode("utf-8")

            if apiData["params"] == "":
                params = None
            else:
                params =json.loads(apiData["params"])

            if apiData["logintype"] == "h5":

                if apiData["headertype"] == "nomal":
                    headers = self.get_token("h5",self.phone)
                elif apiData["headertype"] == "ideamark":
                    headers = self.get_idea_mark_headers("h5",self.phone)
                elif apiData["headertype"] == "unlogin":
                    headers = {"Eaton-Company-CODE":self.code, "Eaton-Origin": "STANDARDH5",'Content-Type': 'application/json;charset=UTF-8'}
                else:
                    headers = self.get_projectid_headers("h5",self.phone)
                print(headers)


                re = s.request(method=method, url=self.url + api, headers=headers,data=data,params=params)
                #print(dump.dump_all(re).decode("utf-8"))
                #print(re.url)
                return re

            else:

                if apiData["headertype"] == "nomal":
                    headers = self.get_token("pc",self.phone)
                elif apiData["headertype"] == "ideamark":
                    headers = self.get_idea_mark_headers("pc",self.phone)
                elif apiData["headertype"] == "unlogin":
                    headers = {"Eaton-Company-CODE":self.code, "Eaton-Origin": "PC",'Content-Type': 'application/json;charset=UTF-8'}
                else:
                    headers = self.get_projectid_headers("pc",self.phone)
                print(headers)
                re = s.request(method=method, url=self.url + api, headers=headers,data=data,params=params)
                #print(dump.dump_all(re).decode("utf-8"))
                #print(re.url)
                return re
        except Exception as e:
            print(e)


    def newsendRequests(self,s,logintype,headertype,api,method,params,data):
        if logintype == "h5":
            if headertype == "nomal":
                headers = self.get_token("h5", self.phone)
            elif headertype == "ideamark":
                headers = self.get_idea_mark_headers("h5", self.phone)
            elif headertype == "unlogin":
                headers = {"Eaton-Company-CODE":self.code, "Eaton-Origin": "STANDARDH5",'Content-Type': 'application/json;charset=UTF-8'}
            else:
                headers = self.get_projectid_headers("h5", self.phone)

            re = s.request(url = self.url+api,method=method,headers=headers,params=params,data=data)
            #print(dump.dump_all(re).decode("utf-8"))
            #print(re.url)
            return re

        else:
            if headertype == "nomal":
                headers = self.get_token("pc", self.phone)
            elif headertype == "ideamark":
                headers = self.get_idea_mark_headers("pc", self.phone)
            elif headertype == "unlogin":
                headers = {"Eaton-Company-CODE":self.code, "Eaton-Origin": "PC",'Content-Type': 'application/json;charset=UTF-8'}
            else:
                headers = self.get_projectid_headers("pc", self.phone)
            re = s.request(url=self.url + api, method=method, headers=headers, params=params, data=data)
            return re




#调试用
if __name__ == "__main__":
    pass



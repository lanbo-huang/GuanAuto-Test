from send_request import SendRequests
from readxls import ReadExcel
from jsonpath_rw import  parse
import requests,json

class Depend():
    def __init__(self,filename,phone):
        self.readxls = ReadExcel(filename)
        self.send_request = SendRequests(phone)
        self.phone = phone


    def run_depend_case(self,caseid):
        """
        执行依赖case，获取执行结果
        :return:
        """
        s = requests.session()
        row_datas = self.readxls.get_row_data(caseid)[0]
        api = row_datas["url"]
        method = row_datas["method"]
        logintype = row_datas["logintype"]
        headertype = row_datas["headertype"]


        params = row_datas["params"]
        if params == "":
            params = None
        else:
            params = json.loads(params)

        data = row_datas["data"]
        if data == "":
            data = None
        else:
            data = json.loads(data)

        res = self.send_request.newsendRequests(s,logintype,headertype,api,method,params,data).json()
        return res

    def get_depend_rundata(self,caseid,key):
        res = self.run_depend_case(caseid)#依赖case的返回值
        json_exe = parse(key)#通过json_path_rw 的方式去匹配结果
        result = json_exe.find(res)
        result_data = [data.value for data in result][0]
        return result_data




























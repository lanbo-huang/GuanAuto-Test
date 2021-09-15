import os,sys,configparser

'''sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tool import Parameter as t
from lib import Public as  p'''

from Guan.lib.Public import Public as p
from Guan.tool import  Parameter as t
print(os.path.dirname(os.path.dirname(__file__)))

def Inaddcust(headers):
    text = "内场新增客户"
    api = "/api/biz/h5/out/customer/add"
    method = "post"
    data = {}
    p.Request(method,headers,api,data,text)

if __name__ =="__main__":
    P = p()

    headers={
            'Eaton-Company-CODE': 'CSGS',
            'Content-Type': 'application/json;charset=UTF-8',
        "Eaton-Origin":"STANDARDH5"}

    Inaddcust(headers)


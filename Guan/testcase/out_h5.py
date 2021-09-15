import configparser,os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Guan.lib.Public import Request,Get_headers

print(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))





def Api_request(key):
    """
    读取接口配置文件，并发起请求
    :param key:
    :return:
    """
    method = cf.get(key,"method")
    headers = Get_headers(url) #默认内场登录请求，可以通过更改账号方式确认
    api = cf.get(key,"api")
    keyword = cf.get(key,"keyword")
    params = cf.get(key,"params")
    data = cf.get(key,"data")
    Request(method,headers,api,keyword,params,data)



cf = configparser.ConfigParser()
base_dir = os.path.dirname(os.path.dirname(__file__))
cf.read(os.path.join(base_dir, "api", "out_api.ini"), encoding="utf-8")

url = cf.get("server","url")


list = cf.sections()
print(list)

num = len(list)
for i in range(num-1):
    key = list[1+i]
    Api_request(key)



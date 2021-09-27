import unittest,requests
from ddt import  ddt,data
from send_request import  SendRequests
from requests_toolbelt.utils import dump

send_request = SendRequests("13300000109")

url = send_request.url + "/api/biz/h5/out/customer/custList"




@ddt
class Test_01(unittest.TestCase):
    @data(1,2,3,4,5)
    def test_01(self,value):
        headers = send_request.get_projectid_headers("h5","13300000109")
        paramas = {"codShare": "3",
                   "menuType": "1",
                   "timeType": "DAT_CREATE",
                   "followType": value,
                   "pageNo": "1",
                   "pageSize": "10"}
        res = requests.get(url=url, params=paramas, headers =headers)
        print(dump.dump_all(res).decode("utf-8"))



if __name__ == "__main__":
    unittest.main()





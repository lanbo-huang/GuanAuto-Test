import requests,json
url ="https://test.guan.yatonghui.com/api/biz/h5/cust/booking/room/saveFlux"

headers ={
    "Eaton-Company-CODE": "BNHJT",
    "Eaton-Origin": "H5",
    'Content-Type': 'application/json;charset=UTF-8'
}


data={
"codPrjName": "香麓山",
"codPrjId": "168",
"custName": "RR",
"custPhone": "13313131314",
"assumpsitDate": "2020-07-09 12:00:00",
"fluxId": "201922232131235"
}


re=requests.post(url=url,headers=headers,data=json.dumps(data))
print(re.status_code)
print(re.content.decode())

import requests,re

url = "http://fund.eastmoney.com/company/default.html#scomscope;ddesc"

res = requests.get(url).content.decode()
#(res)
x=re.findall(r'//*[@id="gspmTbl"]/tbody/tr[1]/td[2]/a',res)

print(x)
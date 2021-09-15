import random,time,datetime,os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
def Getphone(prenums):
    phone = prenums+time.strftime("%d%H%M%S")
    return phone
def Getname(type):
    namCustZh = type + time.strftime("%m%d%H%M%S")
    return namCustZh

def Getdate():
    assumpsitDate = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    return assumpsitDate

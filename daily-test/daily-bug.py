#codig:utf-8
from jira import JIRA
#import time,datetime
#c_time = datetime.datetime.now()
#today = datetime.datetime.now().strftime("%Y-%m-%d")
#torrow = (c_time + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")

def Get_bugs(today,torrow):

    total_bugs ="issuetype = 故障 AND created >=" + today + " AND created <= "+ torrow
    solve_bugs = "issuetype = 故障 AND status = 已关闭 AND created >= " + today + " AND created <= "+ torrow
    unsolve_bugs = "issuetype = 故障 AND status in (新建, 处理中, 重新打开, 挂起, 已接受,已拒绝) AND created >= " + today + " AND created <= "+ torrow
    dyz_bugs = "issuetype = 故障 AND status in (已解决,已验证) AND created >= " + today + " AND created <= "+ torrow


    total_bugs=len(jira.search_issues(total_bugs,maxResults=1000))
    unslove_num=len(jira.search_issues(unsolve_bugs,maxResults=1000))
    slove_num=len(jira.search_issues(solve_bugs,maxResults=1000))
    dyz_num = len(jira.search_issues(dyz_bugs, maxResults=1000))

    print("总bug数 {0}".format(total_bugs))
    print("已关闭bug数 {0}".format(slove_num))
    print("待解决bug数:{0}".format(unslove_num))
    print("待验证bug数:{0}".format(dyz_num))




jira =JIRA(server='http://39.108.220.162:8888',basic_auth=('huangwangyuan','a123456'))
c="2020-08-1"
t="2020-08-30"
Get_bugs(c,t)






#for ver in jira.project(10100).versions:
 #   print(ver)

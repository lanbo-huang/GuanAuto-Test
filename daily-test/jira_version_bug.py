#codig:utf-8
from jira import JIRA

def Get_bugs(versions):
    #版本未关闭的bug数据
    num = len(versions)
    for i in range(num):
        version = versions[i]
        #print(version)
        all_bug="project = GUAN AND issuetype = 故障 AND status in (新建, 处理中, 重新打开, 已解决, 已接受, 已验证) AND affectedVersion = "+ version
        #print(all_bug)
        unslove_bug = "project = GUAN AND issuetype = 故障 AND status in (新建, 处理中, 重新打开, 已接受) AND affectedVersion = "+ version
        unclose_bug = "project = GUAN AND issuetype = 故障 AND status in (已解决) AND affectedVersion = "+ version
        sum_bugs = "project = GUAN AND issuetype = 故障  AND affectedVersion = "+ version

        #all= jira.search_issues(all_bug,maxResults=1000)
        unslove=jira.search_issues(unslove_bug,maxResults=1000)
        unclose=jira.search_issues(unclose_bug,maxResults=1000)
        bugs = jira.search_issues(sum_bugs,maxResults=1000)


        total_bugs=len(bugs)
        unclose_num=len(unclose)
        unslove_num=len(unslove)

        print("{0}版本缺陷情况如下:".format(version))
        print("待修复的bug数 {0}".format(unslove_num))
        print("待关闭的bug数 {0}".format(unclose_num))
        print("bug总数:{0}".format(total_bugs))
        print("\n")



jira =JIRA(server='http://39.108.220.162:8888',basic_auth=('huangwangyuan','a123456'))
#versions=["观系统-现网V1.2.2-数据统计优化","标准版手机端（v1.0.3-v1.0.4）","积分商城","观系统-现网V1.2.3","标准化产品PC迭代V1.3.1（导入导出日志）"]
#Get_bugs(versions)



for ver in jira.project(10100).versions:
    print(ver)

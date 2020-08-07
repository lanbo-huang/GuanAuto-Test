import pymysql
#链接数据库
def mysql_connect():
    #1、测试环境数据库
    conn = pymysql.connect(host='rm-wz98ju5jwvu87p8l86o.mysql.rds.aliyuncs.com',user="local_develop",password="Ytonghui&!local2020",database="guan_pre",charset="utf8")
    #2、生产环境数据库
    #conn = pymysql.connect(host='rm-wz96xqxw14qo6edaxio.mysql.rds.aliyuncs.com', user="hwy",password="HWY@112233", database="guan_prod", charset="utf8")
    return conn

#删除数据
def delete_data(sql):
    conn= mysql_connect()
    curson=conn.cursor()
    try:
        curson.execute(sql)
    except Exception as e:
        print(e)
    conn.commit()
    conn.close()

#取报备id
def get_id(sql):
    conn = mysql_connect()
    curson = conn.cursor()
    try:
        curson.execute(sql)
        id = curson.fetchone()[0]
        conn.close()
        return id
    except Exception as e:
        print(e)





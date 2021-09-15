import configparser
cf = configparser.ConfigParser()
cf.read("config.ini")
secs = cf.sections() #取配置文件中的主标识
options = cf.options("api")#取标识文件中的内容
print(options)

item = cf.items("api") #取标识中的键值
print(item)

host = cf.get("api","host") #取具体的值
print(host)

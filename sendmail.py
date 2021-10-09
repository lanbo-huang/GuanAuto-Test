#!/usr/bin/env python
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import setting
import smtplib
from newReport import new_report
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(file_new):
    """
    定义发送邮件
    :param file_new:
    :return: 成功：打印发送邮箱成功；失败：返回失败信息
    """
    f = open(file_new,'rb')
    mail_body = f.read()
    f.close()
    #发送附件
    report = new_report(setting.TEST_REPORT)#取出最新的报告
    sendfile = open(report,'rb').read()

    att = MIMEText(sendfile,'base64','utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att.add_header("Content-Disposition", "attachment", filename=("gbk", "", report))

    msg = MIMEMultipart('related')
    msg.attach(att)
    msgtext = MIMEText(mail_body,'html','utf-8')
    msg.attach(msgtext)
    msg['Subject'] = "观系统H5_外场接口测试报告,测试请忽略!"
    msg['from'] = "huangwangyuan@szeaton.com"

    #定义邮箱信息
    mail_host = "smtp.exmail.qq.com"
    mail_pass="TEiYtg2fEXAc3soM"
    sender="huangwangyuan@szeaton.com"
    #receivers=["huangwangyuan@szeaton.com","jiangcheng@szeaton.com","leilei@szeaton.com","liaojiahong@szeaton.com","wangkun@szeaton.com","dongfei@szeaton.com","gushiyang@szeaton.com"]
    receivers_02 = ["huangwangyuan@szeaton.com"]
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(sender, mail_pass)
        smtpObj.sendmail(sender, receivers_02, msg.as_string())
        smtpObj.quit()
        print('邮件发送成功')
    except Exception as  e:
        print("失败: " + str(e))

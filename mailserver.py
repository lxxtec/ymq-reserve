# -*- encoding: utf-8 -*-
'''
@File    : email.py
@Time    : 2022/11/29 18:03:49
@Author  : lxxtec
@Contact : 631859877@qq.com
@Version : 0.1
@Desc    : None
'''
import smtplib
from email.header import Header
from email.mime.text import MIMEText


class MailServe:
    def __init__(self) -> None:
        self.smtp = smtplib.SMTP()
        self.user = "lxxtec@126.com"
        self.passwd = "YFBBYRMSCEMOVTFY"

    def send_mail(self, msg, subject, toWho):
        # 创建 SMTP 对象
        smtp = smtplib.SMTP()
        # 连接（connect）指定服务器
        smtp.connect("smtp.126.com", port=25)
        # 登录，需要：登录邮箱和授权码
        smtp.login(user=self.user, password=self.passwd)
        message = MIMEText(msg, 'plain', 'utf-8')
        message['From'] = Header("lxxtec", 'utf-8')  # 发件人的昵称
        message['To'] = Header("aaa", 'utf-8')  # 收件人的昵称
        message['Subject'] = Header(subject, 'utf-8')  # 定义主题内容
        # print(message)
        smtp.sendmail(from_addr=self.user,
                      to_addrs=toWho, msg=message.as_string())


if __name__ == "__main__":
    ser = MailServe()
    ser.send_mail('<h2>test email<h2/>',
                  "[HEU 场地预定app] 预定结果", '631859877@qq.com')

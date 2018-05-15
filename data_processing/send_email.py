# -*- coding: utf-8 -*-
# @Time    : 4/28/2018 10:07 AM
# @Author  : sunyonghai
# @File    : send_email.py
# @Software: ZJ_AI

import smtplib
from email.mime.text import MIMEText

def notify(content):
    msg_from = '931103972@qq.com'  # 发送方邮箱
    passwd = 'nrpsrzgwsmssbahf'  # 填入发送方邮箱的授权码
    # msg_to = '931103972@qq.com, 841861601@qq.com,2092089369@qq.com'  # 收件人邮箱
    msg_to = ['841861601@qq.com','2092089369@qq.com', '931103972@qq.com'] # 收件人邮箱

    subject = "Data preprocessing for label"  # 主题
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    # msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print('Send email successful')
    except Exception as ex :
        print( 'Failed:'.format(ex))
    finally:
        s.quit()

if __name__ == '__main__':
    content = 'hello, send by Python...'
    notify(content)
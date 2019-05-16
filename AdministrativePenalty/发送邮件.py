# coding:utf-8
import yagmail
# 1. 发送邮件
# 　　最开始想到的当然是怎么用Python把邮件发送出去了，用的是yagmail库。首先安装yagmail库

# 登录你的邮箱
yag = yagmail.SMTP(user = '787190277@qq.com', password = 'zcyuukrskcekbbdc', host = 'smtp.qq.com',smtp_starttls = False)
# 发送邮件
yag.send(to = '787190277@qq.com', subject = '邮件的主题', contents = 'hahaha')
# 登录邮箱
# yagmail.SMTP(user, password, host, port)
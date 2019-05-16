import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def mail(my_sender,my_pass,my_user,Subject,content):
    try:
        msg=MIMEText('%s'%(content),'plain','utf-8')
        msg['From']=formataddr([" ",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr([" ",my_user])      # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']= "%s"%(Subject)        # 邮件的主题，也可以说是标题

        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()# 关闭连接
        print("发送成功")
    except Exception:# 如果 try 中的语句没有执行，则会执行下面的 ret=False
        print("发送失败")


my_sender = '13458956855@qq.com'  # 发件人邮箱账号
my_pass = 'vfqnxbhkasnvbfha'  # 发件人邮箱密码(当时申请smtp给的口令)
my_user = '13458956855@qq.com'  # 收件人邮箱账号，我这边发送给自己
Subject = "本次测试"  # 邮件的主题，邮件的标题
content = "shiyishis " # 邮件的内容
mail(my_sender,my_pass,my_user,Subject,content)
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.message import EmailMessage


# Open the plain text file whose name is in textfile for reading.
def send_mail(subject, content, mail):
    msg = EmailMessage()
    msg.set_content(content)
    smtp_server = 'smtp.xiaoxiangyoupin.cn'
    me = 'bj@xiaoxiangyoupin.cn'
    you = mail

    #三要素，标题，发送者，收件人
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you

    # Send the message via our own SMTP server.
    s = smtplib.SMTP_SSL(host=smtp_server, port=465)
    s.login(user=me, password='Yuanshi@123')#我们的邮箱服务器邮件发送的时候要验证
    try:
        s.send_message(msg)
    except Exception as e:
        output = str(e) + '邮件发送失败，检查邮箱地址是否填错'
        return output
    else:
        s.quit()
        return "邮件发送成功"


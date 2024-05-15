import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email(title, content, receiver):
    send_gmail_user = 'cckuan10@gmail.com'
    # send_gmail_password = 'zcdgjpgnnkcgyizj'
    send_gmail_password = 'ghlc uvmx vkrl swgz'
    rece_gmail_user = receiver

    msg = MIMEText(content, 'plain', 'utf-8')  # 內文
    msg['Subject'] = f'{title}' # 標題
    msg['From'] = send_gmail_user
    msg['To'] = rece_gmail_user

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(send_gmail_user, send_gmail_password)
    server.send_message(msg)
    server.quit()

# send_mail_for_me('你好呀旅行者', '狩獵開始了')
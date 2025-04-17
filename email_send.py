import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback

class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.163.com"
        self.smtp_port = 465
        # self.sender_email = "ttxh09@163.com"
        self.sender_email = "ttxh10@163.com"
        # self.sender_password = "WWUmUWcnCRRWuRQu"  # 09
        self.sender_password = "KZqMvSquNnci58yD"  # 10
        self.receiver = "akane.s@qq.com"

        # ----------------
        self.smtp_server = "smtp.163.com"
        self.smtp_port = 465
        self.sender_email = "ttxh10@163.com"
        self.sender_password = "KZqMvSquNnci58yD"  # 10
        self.receiver = "akane.s@qq.com"


    def send_email(self, subject, body):
        try:
            # 创建邮件消息
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.receiver
            msg['Subject'] = subject

            # 添加邮件正文
            msg.attach(MIMEText(body, 'plain'))

            # 连接SMTP服务器并发送邮件
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            print("✅ 邮件发送成功！")
            return True

        except smtplib.SMTPException as e:
            print(traceback.format_exc())
            return False


# 示例用法
if __name__ == "__main__":

    email_sender = EmailSender()

    # 发送邮件
    success = email_sender.send_email(
        subject="测试邮件2",
        body="test"
    )

    if success:
        print("📧 邮件发送流程完成。")
    else:
        print("⚠️ 邮件发送过程中出现问题。")

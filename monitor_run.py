import psutil
import time
from email_send import EmailSender  # 导入你的邮件发送类


class ProcessMonitor:

    def __init__(self, target_keyword, email_sender, check_interval=60):
        self.target_keyword = target_keyword
        self.email_sender = email_sender
        self.check_interval = check_interval

    def is_process_running(self):

        for process in psutil.process_iter(['pid', 'cmdline']):
            try:
                cmdline = process.info['cmdline']
                if cmdline and any(self.target_keyword in ' '.join(cmdline) for cmdline_part in cmdline):
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return False

    def monitor(self):
        print(f"🚀 开始监控进程关键字: '{self.target_keyword}'")
        while True:
            if not self.is_process_running():
                print(f"⚠️ 警告: 包含关键字 '{self.target_keyword}' 的进程已停止！发送通知...")
                subject = f"⚠️ 进程已停止"
                body = f"监控的 Python 进程包含关键字 '{self.target_keyword}' 已停止，请立即检查服务器。"
                self.email_sender.send_email(
                    subject=subject,
                    body=body
                )

            time.sleep(self.check_interval)


# -------------------------
# 主程序
# -------------------------
if __name__ == "__main__":

    # 创建邮件发送器实例
    email_sender = EmailSender()

    # 要监控的进程关键字
    TARGET_KEYWORD = "scrapy crawl search"

    # 创建进程监控器实例
    monitor = ProcessMonitor(
        target_keyword=TARGET_KEYWORD,
        email_sender=email_sender,
        check_interval=3600  # 每60秒检查一次
    )

    monitor.monitor()

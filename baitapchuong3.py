import os
import shutil
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")


BACKUP_FOLDER = "backup"


def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("✅ Đã gửi email thông báo thành công.")
    except Exception as e:
        print(f"❌ Gửi email thất bại: {e}")


def backup_database():
    print("🚀 Bắt đầu backup database...")
    try:
        
        files = [f for f in os.listdir() if f.endswith('.sql') or f.endswith('.sqlite3')]
        if not files:
            raise Exception("Không tìm thấy file .sql hoặc .sqlite3 để backup.")

        
        if not os.path.exists(BACKUP_FOLDER):
            os.makedirs(BACKUP_FOLDER)

        for file in files:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{os.path.splitext(file)[0]}_{timestamp}{os.path.splitext(file)[1]}"
            shutil.copy(file, os.path.join(BACKUP_FOLDER, backup_file))
            print(f"✅ Đã backup: {file} -> {backup_file}")

        send_email("Backup Database Thành Công", "Backup database thành công lúc 00:00 AM.")
    except Exception as e:
        print(f"❌ Lỗi backup: {e}")
        send_email("Backup Database Thất Bại", f"Lỗi backup: {e}")


schedule.every().day.at("00:00").do(backup_database)

print("🕛 Đang chờ đến 00:00 để backup database...")
while True:
    schedule.run_pending()
    time.sleep(1)

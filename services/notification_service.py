import dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

dotenv.load_dotenv('.env') # load the content of the environment variable

class NotificationService:

    @staticmethod
    def send_email(subject, body, receiver):
        print("email method")
        SMTP_SERVER = "smtp.gmail.com" 
        SMTP_PORT =  465
        EMAIL_SENDER = "emehinolasam01@gmail.com"
        EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD") # email password is stored in .env file
        EMAIL_RECEIVER = receiver

        # Create email
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = f"{subject} 📢"

        # Email body
        body = body
        msg.attach(MIMEText(body, "plain"))

        # Send email
        try:
            print("Sending email...")
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
            print("Connected to server")
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
            # server.quit()
            print("✅ Email sent successfully!")
        except Exception as e:
            print(f"❌ Error: {e}")

    
    @staticmethod
    def create_inapp_message():
        pass
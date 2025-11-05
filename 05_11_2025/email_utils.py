import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

def send_email_smtp(to_email, subject, body, from_email=None, app_password=None):
    if from_email is None:
        from_email = os.getenv('GMAIL_ADDRESS')
    if app_password is None:
        app_password = os.getenv('GMAIL_APP_PASSWORD')
    if not from_email or not app_password:
        print("❌ Gmail credentials missing. Set GMAIL_ADDRESS and GMAIL_APP_PASSWORD in environment.")
        return False
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #f8f9fa; padding: 30px; border-radius: 10px;">
                    <h2 style="color: #2c3e50;">🎉 Congratulations!</h2>
                    <div style="margin: 20px 0; line-height: 1.6;">
                        {body.replace(chr(10), '<br>')}
                    </div>
                </div>
            </body>
        </html>
        """
        part1 = MIMEText(body, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(from_email, app_password)
            smtp_server.sendmail(from_email, to_email, msg.as_string())
        print(f"✅ Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

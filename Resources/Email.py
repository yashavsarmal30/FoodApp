import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, Tuple
from dotenv import load_dotenv
import platform
from services.ip_location import ip_location_service
 
load_dotenv()   # Email Credentials Stored in .env

def send_mail(to: str = '', subject: str = '', content: str = '', attachment: Optional[Tuple[bool, str]] = (False, '')):
    msg = MIMEMultipart('alternative')
    msg['From'] = os.getenv('Email')
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(content, 'plain'))

    if content:
        msg.attach(MIMEText(content, 'html'))

    attachment_enabled, attachment_path = attachment
    if attachment_enabled:
        with open(attachment_path, "rb") as attachment_file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment_file.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {attachment_path}",
            )
            msg.attach(part)

    try:
        # Reuse SMTP connection
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(os.getenv('Email'), os.getenv('Password'))
            # Send email
            server.sendmail(os.getenv('Email'), to, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def SendLoginAlert(user_data):
    try:
        system_details = {
            'OS': platform.system(),
            'OS Version': platform.version(),
            'Machine': platform.machine(),
            'Processor': platform.processor(),
            'IP': ip_location_service._get_cached_or_fetch('ip') or "Unknown"
        }
        
        IpMessage = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login Alert</title>
        <style>
            body, html {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                line-height: 1.6;
            }}
            
            .wrapper {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            
            .alert-box {{
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                color: #721c24;
                padding: 15px;
                margin-bottom: 20px;
                border-radius: 5px;
            }}
            
            .footer {{
                text-align: center;
                margin-top: 20px;
                color: #777;s
            }}
        </style>
    </head>
    <body>
        <div class="wrapper">
            <div class="header">
                <h1>Login Alert</h1>
            </div>
            <div class="alert-box">
                <p>A login has been received from account <a href="{user_data['Email']}">{user_data['Email']}</a>:</p>
                <ul>
                    <li><strong>IP Address:</strong> <a href="{system_details['IP']}">{system_details['IP']}</a></li>
                    <li><strong>Device:</strong> {system_details['OS']} {system_details['OS Version']}</li>
                    <li><strong>Machine:</strong> {system_details['Machine']}</li>
                    <li><strong>Processor:</strong> {system_details['Processor']}</li>
                </ul>
            </div>
            <div class="footer">
                <p>This email is autogenerated. Please do not reply.</p>
            </div>
        </div>
    </body>
    </html>
    """
        send_mail(to=user_data['Email'],subject="Login Alert",content=IpMessage)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == '__main__':
   print("Run >>>>>>>>  main.py <<<<<<<< File")
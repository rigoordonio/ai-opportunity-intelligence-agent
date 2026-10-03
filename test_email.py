from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText

load_dotenv()

sender = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASS")

receiver = "rigoordonio@gmail.com"

report = """
🚨 Shell Opportunity Alert

Shell announced a new LNG expansion project.

Relevant Bilfinger Services:
- Asset Integrity
- Inspection
- Mechanical Maintenance

Opportunity Rating: HIGH

Recommended Action:
Review project stakeholders and contracting strategy.
"""

msg = MIMEText(report)

msg["Subject"] = "✅ AI Bot Test"
msg["From"] = sender
msg["To"] = receiver

smtp = smtplib.SMTP("smtp.gmail.com", 587)
smtp.starttls()

smtp.login(sender, password)

smtp.send_message(msg)

smtp.quit()

print("✅ Email sent successfully")
import subprocess
import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText

# Load environment variables
load_dotenv()

sender = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASS")

# Sample news input
news = """
Shell announced FEED activities for a new LNG expansion project.
Expected CAPEX exceeds $3 billion.
The project is expected to support increased LNG export capacity.
"""

# VP Business Development prompt
prompt = f"""
You are a Business Development Intelligence Analyst supporting the
President, SVP Business Development and Regional Managing Directors.

IMPORTANT:
Return FINAL ANSWER ONLY.
Do not show reasoning.
Do not show thinking.
Do not explain analysis.
Do not use markdown.
Keep response under 50 words.

Format exactly:

ACCOUNT:
HEADLINE:
OPPORTUNITY:
SCORE:
ACTION:

News:
{news}
"""

# Run Qwen
result = subprocess.run(
    ["ollama", "run", "qwen3:14b", prompt],
    capture_output=True,
    text=True
)

report = result.stdout

# Remove Qwen thinking section
if "...done thinking." in report:
    report = report.split("...done thinking.")[-1]

if "Thinking..." in report:
    report = report.replace("Thinking...", "")

report = report.strip()

# Fallback if model returns empty output
if not report:
    report = """
ACCOUNT: Shell

HEADLINE:
$3B+ LNG expansion enters FEED stage.

OPPORTUNITY:
Asset Integrity, Inspection, Mechanical Maintenance and Asset Performance services.

SCORE:
9/10

ACTION:
Engage FEED stakeholders and monitor EPC awards.
"""

# Build email
msg = MIMEText(report)

msg["Subject"] = "🚨 Daily Opportunity Intelligence"
msg["From"] = sender
msg["To"] = sender

# Send email
smtp = smtplib.SMTP("smtp.gmail.com", 587)
smtp.starttls()

smtp.login(sender, password)

smtp.send_message(msg)

smtp.quit()

print("✅ Daily Opportunity Intelligence Email Sent")
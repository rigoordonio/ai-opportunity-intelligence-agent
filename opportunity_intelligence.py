import feedparser
import subprocess
import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText

# Load Gmail credentials
load_dotenv()

sender = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASS")

# Pull live news
feed = feedparser.parse(
    "https://news.google.com/rss/search?q=Shell+LNG"
)

if len(feed.entries) == 0:
    news = "No recent Shell news found."
else:
    news = feed.entries[0].title

# Executive prompt
prompt = f"""
You are an Executive Business Development Intelligence Analyst for Bilfinger.

Audience:
- SVP Business Development
- President Asset Performance
- Regional Managing Directors

Return ONLY:

ACCOUNT:
HEADLINE:
OPPORTUNITY:
SCORE:
ACTION:

Maximum 50 words.

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

# Remove Qwen thinking output
if "...done thinking." in report:
    report = report.split("...done thinking.")[-1]

if "Thinking..." in report:
    report = report.replace("Thinking...", "")

report = report.strip()

# Build email
msg = MIMEText(report)

msg["Subject"] = "🚨 Daily Opportunity Intelligence"
msg["From"] = sender
msg["To"] = sender

smtp = smtplib.SMTP("smtp.gmail.com", 587)
smtp.starttls()

smtp.login(sender, password)

smtp.send_message(msg)

smtp.quit()

print("✅ Daily Opportunity Intelligence Sent")
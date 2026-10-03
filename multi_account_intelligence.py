import feedparser
import subprocess
import os
import smtplib
import re

from urllib.parse import quote
from dotenv import load_dotenv
from email.mime.text import MIMEText
from datetime import datetime

# ===================================
# LOAD EMAIL SETTINGS
# ===================================

load_dotenv()

sender = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASS")

# ===================================
# EMAIL RECIPIENTS
# ===================================

recipients = [
    "rigoordonio@gmail.com",
    "ruairi.kerr@bilfinger.com"
]

# ===================================
# TARGET ACCOUNTS
# ===================================

accounts = {
    "Shell": "Shell LNG project",
    "ADNOC": "ADNOC capital investment",
    "Aramco": "Aramco project award",
    "Woodside": "Woodside LNG development",
    "Petrofac": "Petrofac contract award"
}

# ===================================
# DATE
# ===================================

today = datetime.now().strftime("%d-%b-%Y")

# ===================================
# EMAIL HEADER
# ===================================

email_body = f"""
🚨 DAILY OPPORTUNITY INTELLIGENCE

Date: {today}

================================================

"""

# ===================================
# PROCESS ACCOUNTS
# ===================================

for account, query in accounts.items():

    try:

        encoded_query = quote(query)

        feed = feedparser.parse(
            f"https://news.google.com/rss/search?q={encoded_query}"
        )

        if len(feed.entries) == 0:
            continue

        news = feed.entries[0].title

        prompt = f"""
You are a VP Business Development Intelligence Analyst.

Your audience:
- SVP Business Development
- President Asset Performance
- Regional Managing Directors

Return ONLY:

ACCOUNT:
HEADLINE:
WHY IT MATTERS:
OPPORTUNITY:
SCORE:
ACTION:

Maximum 75 words.

No thinking.
No reasoning.
No explanation.
No markdown.

Account:
{account}

News:
{news}
"""

        result = subprocess.run(
            ["/opt/homebrew/bin/ollama", "run", "qwen3:14b", prompt],
            capture_output=True,
            text=True
        )

        report = result.stdout

        # ===================================
        # CLEAN OLLAMA OUTPUT
        # ===================================

        if "...done thinking." in report:
            report = report.split("...done thinking.")[-1]

        if "Thinking..." in report:
            report = report.replace("Thinking...", "")

        # Remove ANSI escape sequences
        report = re.sub(
            r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])',
            '',
            report
        )

        # Remove artifacts such as:
        # [8D[K
        # [4D[K
        # [11D[K
        report = re.sub(r'\[\d+[A-Z]', '', report)
        report = re.sub(r'\[K', '', report)

        report = report.strip()

        # ===================================
        # FALLBACK
        # ===================================

        if len(report) < 10:

            report = f"""
ACCOUNT:
{account}

HEADLINE:
{news}

WHY IT MATTERS:
Potential strategic growth signal.

OPPORTUNITY:
Review Bilfinger service alignment.

SCORE:
N/A

ACTION:
Manual review recommended.
"""

        email_body += report
        email_body += "\n\n-------------------------------------\n\n"

    except Exception as e:

        email_body += f"""
ACCOUNT:
{account}

ERROR:
{str(e)}

-------------------------------------

"""

# ===================================
# DISCLAIMER
# ===================================

email_body += """

================================================

Generated automatically from public news sources
and AI-assisted analysis.

Please independently validate information before
making business decisions.

================================================
"""

# ===================================
# SEND EMAIL
# ===================================

msg = MIMEText(email_body)

msg["Subject"] = f"🚨 Daily Opportunity Intelligence | {today}"
msg["From"] = sender
msg["To"] = ", ".join(recipients)

smtp = smtplib.SMTP("smtp.gmail.com", 587)
smtp.starttls()

smtp.login(sender, password)

smtp.sendmail(
    sender,
    recipients,
    msg.as_string()
)

smtp.quit()

print("✅ Daily Opportunity Intelligence Sent")
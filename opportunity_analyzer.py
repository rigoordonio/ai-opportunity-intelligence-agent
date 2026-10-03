import feedparser
import subprocess

feed = feedparser.parse(
    "https://news.google.com/rss/search?q=Shell+LNG"
)

news = feed.entries[0].title

prompt = f"""
You are an Executive Business Development Intelligence Analyst.

Return only:

ACCOUNT:
HEADLINE:
OPPORTUNITY:
SCORE:
ACTION:

Maximum 50 words.

News:
{news}
"""

result = subprocess.run(
    ["ollama", "run", "qwen3:14b", prompt],
    capture_output=True,
    text=True
)

report = result.stdout

if "...done thinking." in report:
    report = report.split("...done thinking.")[-1]

print(report)
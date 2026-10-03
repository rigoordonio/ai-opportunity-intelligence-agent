import feedparser

feed = feedparser.parse(
    "https://news.google.com/rss/search?q=Shell+LNG"
)

print("\nLATEST SHELL NEWS\n")

for article in feed.entries[:5]:
    print(article.title)
    print(article.link)
    print("-" * 50)
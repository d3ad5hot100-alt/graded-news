import json
import feedparser
from datetime import datetime

with open("scripts/rss_sources.json", "r", encoding="utf-8") as f:
    sources = json.load(f)["sources"]

news_items = []
seen_titles = set()

for source in sources:

    feed = feedparser.parse(source["url"])

    for entry in feed.entries[:20]:

        title = entry.get("title", "").strip()

        if not title:
            continue

        if title.lower() in seen_titles:
            continue

        seen_titles.add(title.lower())

        news_items.append({
            "title": title,
            "source": source["name"],
            "date": str(datetime.now().date()),
            "category": source["category"],
            "region": source["region"],
            "description": entry.get("summary", "")[:300],
            "url": entry.get("link", "#")
        })

news_items = sorted(
    news_items,
    key=lambda x: x["date"],
    reverse=True
)

with open("data/news.json", "w", encoding="utf-8") as f:
    json.dump(news_items, f, indent=2, ensure_ascii=False)

print(f"Saved {len(news_items)} news articles.")
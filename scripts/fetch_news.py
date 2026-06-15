import json
import feedparser
from datetime import datetime, timedelta

# ===================================
# CONFIG
# ===================================

DAYS_TO_KEEP = 7

KEYWORDS = [
    "student",
    "students",
    "study",
    "study abroad",
    "visa",
    "scholarship",
    "education",
    "international",
    "university",
    "higher education",
    "college",
    "canada",
    "uk",
    "united kingdom",
    "australia",
    "usa",
    "united states",
    "germany",
    "new zealand",
    "bangladesh",
    "bangladeshi"
]

BOOST_KEYWORDS = [
    "bangladesh",
    "bangladeshi",
    "canada",
    "uk",
    "united kingdom",
    "australia",
    "usa",
    "united states",
    "germany",
    "new zealand"
]

# ===================================
# LOAD SOURCES
# ===================================

with open(
    "scripts/rss_sources.json",
    "r",
    encoding="utf-8"
) as f:

    sources = json.load(f)["sources"]

cutoff_date = datetime.utcnow() - timedelta(days=DAYS_TO_KEEP)

news_items = []
seen_titles = set()

# ===================================
# COLLECT
# ===================================

for source in sources:

    try:

        feed = feedparser.parse(source["url"])

        for entry in feed.entries[:50]:

            title = entry.get("title", "").strip()

            description = (
                entry.get("summary", "")
                .replace("\n", " ")
                .replace("\r", " ")
            )

            if not title:
                continue

            title_lower = title.lower()
            description_lower = description.lower()

            if title_lower in seen_titles:
                continue

            text = f"{title_lower} {description_lower}"

            score = 0

            for keyword in KEYWORDS:
                if keyword in text:
                    score += 1

            if score == 0:
                continue

            for keyword in BOOST_KEYWORDS:
                if keyword in text:
                    score += 5

            try:

                if hasattr(entry, "published_parsed") and entry.published_parsed:

                    article_date = datetime(
                        *entry.published_parsed[:6]
                    )

                else:

                    article_date = datetime.utcnow()

            except:

                article_date = datetime.utcnow()

            if article_date < cutoff_date:
                continue

            seen_titles.add(title_lower)

            news_items.append({

                "title": title,

                "source": source["name"],

                "date": article_date.strftime("%Y-%m-%d"),

                "category": source["category"],

                "region": source["region"],

                "description": description[:500],

                "url": entry.get("link", "#"),

                "score": score

            })

    except Exception as e:

        print(f"Error: {source['name']} - {e}")

# ===================================
# SORT
# ===================================

news_items.sort(

    key=lambda x: (
        x["score"],
        x["date"]
    ),

    reverse=True

)

# Keep only best 50

news_items = news_items[:50]

for item in news_items:
    del item["score"]

# ===================================
# SAVE
# ===================================

with open(
    "data/news.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        news_items,
        f,
        ensure_ascii=False,
        indent=2
    )

print(
    f"Saved {len(news_items)} articles."
)

import json
import feedparser
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime

# ============================
# Configuration
# ============================

DAYS_TO_KEEP = 7

PRIORITY_KEYWORDS = [
    "bangladesh",
    "bangladeshi",
    "study abroad",
    "international student",
    "student visa",
    "scholarship",
    "canada",
    "uk",
    "united kingdom",
    "australia",
    "usa",
    "united states",
    "germany",
    "new zealand",
    "university",
    "higher education"
]

EXCLUDED_KEYWORDS = [
    "colombia",
    "brazil",
    "argentina",
    "ecuador",
    "peru",
    "africa",
    "latin america"
]

# ============================
# Load Sources
# ============================

with open(
    "scripts/rss_sources.json",
    "r",
    encoding="utf-8"
) as f:

    sources = json.load(f)["sources"]

# ============================
# Helpers
# ============================

cutoff_date = datetime.utcnow() - timedelta(days=DAYS_TO_KEEP)

news_items = []
seen_titles = set()

# ============================
# Collect News
# ============================

for source in sources:

    try:

        feed = feedparser.parse(source["url"])

        for entry in feed.entries:

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

            # Duplicate check
            if title_lower in seen_titles:
                continue

            # Exclude irrelevant regions
            if any(
                keyword in title_lower
                or keyword in description_lower
                for keyword in EXCLUDED_KEYWORDS
            ):
                continue

            # Keep only relevant content
            relevance_score = 0

            for keyword in PRIORITY_KEYWORDS:

                if (
                    keyword in title_lower
                    or keyword in description_lower
                ):
                    relevance_score += 1

            if relevance_score == 0:
                continue

            # Date parsing
            try:

                if "published_parsed" in entry:

                    article_date = datetime(
                        *entry.published_parsed[:6]
                    )

                elif "published" in entry:

                    article_date = parsedate_to_datetime(
                        entry.published
                    )

                else:

                    article_date = datetime.utcnow()

            except Exception:

                article_date = datetime.utcnow()

            # Only keep last 7 days
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

                "score": relevance_score

            })

    except Exception as e:

        print(
            f"Failed source: {source['name']} - {e}"
        )

# ============================
# Sort News
# ============================

news_items.sort(

    key=lambda x: (
        x["score"],
        x["date"]
    ),

    reverse=True

)

# Remove internal score
for item in news_items:
    item.pop("score", None)

# ============================
# Save
# ============================

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
    f"Saved {len(news_items)} relevant articles."
)

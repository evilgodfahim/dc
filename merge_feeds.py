import feedparser
import hashlib
from datetime import datetime
from feedgen.feed import FeedGenerator

# List of PolitePol feeds
FEED_URLS = [
    "https://politepol.com/fd/WmvWYZRGs2N6.xml",
    "https://politepol.com/fd/25boQpfZBabR.xml",
    "https://politepol.com/fd/AbzelJuwQDQt.xml",
    "https://politepol.com/fd/HTCZfZX3zUiP.xml",
    "https://politepol.com/fd/V2zjj0jzIJXU.xml",
    "https://politepol.com/fd/gmdHnq4z4A0v.xml",
    "https://politepol.com/fd/uZPdh7cAyJmp.xml",
    "https://politepol.com/fd/KVUmtTdIY2kJ.xml",
    "https://politepol.com/fd/e7lvrgKqMQ4M.xml",
    "https://politepol.com/fd/T0IckaBLA4UG.xml",
    "https://politepol.com/fd/7tFz8Diw7Gy6.xml"
]

def main():
    fg = FeedGenerator()
    fg.title("Merged PolitePol Feed")
    fg.link(href="https://yourusername.github.io/your-repo/merged.xml", rel="self")
    fg.description("Aggregated RSS from PolitePol sources")
    fg.language("en")

    seen = set()
    all_entries = []

    for url in FEED_URLS:
        print(f"Fetching {url}")
        try:
            feed = feedparser.parse(url)
            print(f" → {len(feed.entries)} entries")
            for entry in feed.entries:
                link = entry.get("link", "")
                if not link:
                    continue
                uid = hashlib.md5(link.encode("utf-8")).hexdigest()
                if uid not in seen:
                    seen.add(uid)
                    all_entries.append(entry)
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # Sort entries by published date (fall back to updated date or now)
    def get_date(entry):
        return entry.get("published_parsed") or entry.get("updated_parsed") or datetime.utcnow().timetuple()

    all_entries.sort(key=get_date, reverse=True)

    # Limit to latest 100 items
    all_entries = all_entries[:100]

    for entry in all_entries:
        fe = fg.add_entry()
        fe.title(entry.get("title", "No title"))
        fe.link(href=entry.get("link", ""))
        fe.description(entry.get("summary", ""))
        if "published" in entry:
            fe.pubDate(entry.published)

    fg.rss_file("merged.xml")

if __name__ == "__main__":
    main()

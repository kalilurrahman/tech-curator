import feedparser
from datetime import datetime
import time
from app.services.llm import summarize_text

FEEDS = [
    "http://feeds.feedburner.com/TechCrunch/",
    "https://www.theverge.com/rss/index.xml",
    "https://news.ycombinator.com/rss"
]

def fetch_news() -> list[dict]:
    articles = []
    for url in FEEDS:
        try:
            print(f"Polling {url}...")
            feed = feedparser.parse(url)
            for entry in feed.entries[:4]: # Limit for speed
                content = getattr(entry, 'summary', '') or getattr(entry, 'description', '')
                clean_content = content.replace('<p>', '').replace('</p>', '')
                summary = summarize_text(clean_content[:500], feed.feed.title)
                
                articles.append({
                    "title": entry.title,
                    "url": entry.link,
                    "source": feed.feed.title,
                    "published_at": datetime.now(),
                    "content": clean_content,
                    "summary": summary
                })
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            
    return articles

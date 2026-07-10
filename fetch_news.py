import feedparser
import json
import os
import time
import socket
from datetime import datetime

# Set a strict 10-second network timeout so a single dead feed won't freeze the script
socket.setdefaulttimeout(10)

RSS_FEEDS = {
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "VentureBeat AI": "https://venturebeat.com/category/ai/feed/",
    "MIT Technology Review AI": "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
    "ArXiv cs.AI": "http://export.arxiv.org/rss/cs.AI",
    "The Verge AI": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "Google News AI": "https://news.google.com/rss/search?q=artificial+intelligence"
}

CACHE_FILE = "news_cache.json"

def fetch_feed_with_retry(source_name, feed_url, max_retries=3, backoff_delay=2):
    """Attempts to download an RSS feed up to max_retries times with a linear backoff delay."""
    for attempt in range(1, max_retries + 1):
        try:
            feed = feedparser.parse(feed_url)
            
            # feedparser encapsulates network exceptions inside the 'bozo' flag properties
            if feed.bozo and hasattr(feed, 'bozo_exception') and isinstance(feed.bozo_exception, (socket.timeout, TimeoutError)):
                raise feed.bozo_exception
                
            return feed
        except (socket.timeout, TimeoutError, Exception) as e:
            print(f"[{source_name}] Attempt {attempt}/{max_retries} failed: {e}")
            if attempt < max_retries:
                time.sleep(backoff_delay * attempt)
            else:
                print(f"❌ Error: Skipping {source_name} after {max_retries} failed connection attempts.")
    return None

def fetch_ai_news():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            try:
                cached_news = json.load(f)
            except json.JSONDecodeError:
                cached_news = []
    else:
        cached_news = []

    seen_urls = {article.get("link") for article in cached_news if "link" in article}
    new_articles = []

    for source_name, feed_url in RSS_FEEDS.items():
        print(f"Fetching news from {source_name}...")
        feed = fetch_feed_with_retry(source_name, feed_url)
        
        if not feed or not hasattr(feed, 'entries'):
            continue
        
        for entry in feed.entries:
            try:
                # Malformed entry guard: Verify critical attributes exist
                link = getattr(entry, 'link', None)
                title = getattr(entry, 'title', None)
                
                if not link or not title:
                    # Skip incomplete entries silently
                    continue
                
                if link in seen_urls:
                    continue
                
                summary = getattr(entry, 'summary', getattr(entry, 'description', 'No summary available'))
                published_date = getattr(entry, 'published', getattr(entry, 'updated', datetime.now().isoformat()))
                
                article_data = {
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "published_date": published_date,
                    "source": source_name
                }
                
                new_articles.append(article_data)
                seen_urls.add(link)
                
            except Exception as entry_error:
                # Log entry processing errors and keep parsing the rest of the feed
                print(f"Skipped a malformed entry in {source_name}: {entry_error}")
                continue

    all_articles = cached_news + new_articles

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, indent=4, ensure_ascii=False)
        
    print(f"Update complete! Added {len(new_articles)} new articles. Total in cache: {len(all_articles)}")
    return all_articles

if __name__ == "__main__":
    fetch_ai_news()
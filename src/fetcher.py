import feedparser
import requests

from src.config import load_config


def fetch_rss_news(limit=10):
    """Google News RSS에서 뉴스를 수집합니다."""

    config = load_config()
    rss_url = config["news"]["rss_url"]
    timeout = config["request"]["timeout"]

    response = requests.get(rss_url, timeout=timeout)
    response.raise_for_status()

    feed = feedparser.parse(response.content)

    news_list = []

    for entry in feed.entries[:limit]:
        news = {
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "source": entry.get("source", {}).get("title", "Google News"),
            "collection_method": "rss",
        }

        news_list.append(news)

    return news_list
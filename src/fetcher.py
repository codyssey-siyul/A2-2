import feedparser


GOOGLE_NEWS_RSS_URL = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"


def fetch_rss_news(limit=10):
    """Google News RSS에서 뉴스를 수집합니다."""

    feed = feedparser.parse(GOOGLE_NEWS_RSS_URL)

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
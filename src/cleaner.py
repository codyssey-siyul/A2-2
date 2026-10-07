import re
from datetime import datetime
from email.utils import parsedate_to_datetime

from src.config import load_config

def normalize_text(text):
    """불필요한 공백과 줄바꿈을 정리합니다."""
    if not text:
        return ""

    return re.sub(r"\s+", " ", text).strip()


def normalize_date(date_text):
    """RSS 또는 크롤링 날짜를 ISO 8601 형식으로 변환합니다."""
    if not date_text:
        return None

    # RSS 날짜 형식 처리
    try:
        parsed_date = parsedate_to_datetime(date_text)
        return parsed_date.isoformat()
    except (TypeError, ValueError):
        pass

    # 크롤링 날짜 형식 처리: 2026.10.01
    try:
        parsed_date = datetime.strptime(date_text, "%Y.%m.%d")
        return parsed_date.date().isoformat()
    except (TypeError, ValueError):
        return None


def clean_news(news):
    """뉴스 한 건을 정제합니다."""

    title = normalize_text(news.get("title"))
    link = normalize_text(news.get("link"))
    source = normalize_text(news.get("source"))

    # 필수값이 없으면 사용할 수 없는 데이터로 판단
    if not title or not link:
        return None

    cleaned_news = {
        "title": title,
        "link": link,
        "published": normalize_date(news.get("published")),
        "source": source if source else "알 수 없음",
        "content": normalize_text(news.get("content")),
        "collection_method": news.get("collection_method", "unknown"),
        "collected_at": news.get("collected_at"),
    }

    return cleaned_news

def clean_news_list(news_list):
    """뉴스 목록 전체를 정제하고 중복을 제거합니다."""

    config = load_config()
    duplicate_policy = config["cleaning"]["duplicate_policy"]

    cleaned_list = []
    seen_links = set()

    for news in news_list:
        cleaned_news = clean_news(news)

        # 필수값 누락 등으로 정제되지 않은 데이터 제외
        if cleaned_news is None:
            continue

        # 동일한 링크의 뉴스는 중복으로 판단
        if cleaned_news["link"] in seen_links:
            if duplicate_policy == "skip":
                continue

        seen_links.add(cleaned_news["link"])
        cleaned_list.append(cleaned_news)

    return cleaned_list
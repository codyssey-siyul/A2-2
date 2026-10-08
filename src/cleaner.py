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
    """RSS, 크롤링, ISO 8601 날짜를 표준 형식으로 변환합니다."""
    if not date_text:
        return None

    date_text = str(date_text).strip()

    # RSS 날짜 형식
    try:
        parsed_date = parsedate_to_datetime(date_text)
        return parsed_date.isoformat()
    except (TypeError, ValueError, IndexError):
        pass

    # 날짜만 있는 경우 시간 정보 없이 유지
    try:
        return datetime.strptime(date_text, "%Y-%m-%d").date().isoformat()
    except ValueError:
        pass

    # ISO 8601 날짜/시간
    try:
        parsed_date = datetime.fromisoformat(
            date_text.replace("Z", "+00:00")
        )
        return parsed_date.isoformat()
    except ValueError:
        pass

    # 크롤링 날짜 형식
    try:
        parsed_date = datetime.strptime(date_text, "%Y.%m.%d")
        return parsed_date.date().isoformat()
    except ValueError:
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
    """뉴스 목록을 정제하고 설정된 중복 정책을 적용합니다."""

    config = load_config()
    duplicate_policy = config["cleaning"]["duplicate_policy"]

    if duplicate_policy not in ("skip", "upsert"):
        raise ValueError(f"지원하지 않는 중복 정책: {duplicate_policy}")

    cleaned_by_link = {}

    for news in news_list:
        cleaned_news = clean_news(news)

        if cleaned_news is None:
            continue

        link = cleaned_news["link"]

        if duplicate_policy == "skip" and link in cleaned_by_link:
            continue

        # upsert 정책에서는 동일 링크의 최신 입력값으로 갱신
        cleaned_by_link[link] = cleaned_news

    return list(cleaned_by_link.values())

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://www.korea.kr"
LIST_URL = "https://www.korea.kr/news/policyNewsList.do"


def fetch_policy_news_links(limit=5):
    """정책브리핑 정책뉴스 목록에서 기사 제목과 링크를 수집합니다."""

    response = requests.get(
        LIST_URL,
        timeout=10
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    news_list = []
    seen_links = set()

    # 정책뉴스 개별 기사 링크 찾기
    links = soup.select('a[href*="/news/policyNewsView.do"]')

    for link in links:
        href = link.get("href")

        if not href:
            continue

        full_url = urljoin(BASE_URL, href)

        # 이미 수집한 URL이면 제외
        if full_url in seen_links:
            continue

        # 링크 내부에서 제목 요소 우선 탐색
        title_element = link.find(
            ["strong", "b", "h2", "h3", "h4"]
        )

        if title_element:
            title = title_element.get_text(" ", strip=True)
        else:
            title = link.get_text(" ", strip=True).split("\n")[0]

        if not title:
            continue

        seen_links.add(full_url)

        news_list.append({
            "title": title,
            "link": full_url
        })

        if len(news_list) >= limit:
            break

    return news_list

def fetch_policy_news_article(url):
    """정책브리핑 개별 기사에서 본문과 작성일을 수집합니다."""

    import re

    response = requests.get(
        url,
        timeout=10
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # 기사 본문
    content_element = soup.select_one("div.view_cont")

    if content_element:
        content = content_element.get_text(" ", strip=True)
    else:
        content = ""

    # 작성일: YYYY.MM.DD 형식의 span 찾기
    published = ""

    for span in soup.find_all("span"):
        text = span.get_text(strip=True)

        if re.fullmatch(r"\d{4}\.\d{2}\.\d{2}", text):
            published = text
            break

    return {
        "content": content,
        "published": published
    }

def fetch_policy_news(limit=5):
    """정책브리핑 뉴스를 크롤링하여 완성된 뉴스 목록을 반환합니다."""

    from datetime import datetime, timezone

    # 목록 페이지에서 제목 + URL 수집
    news_links = fetch_policy_news_links(limit)

    news_list = []
    collected_at = datetime.now(timezone.utc).isoformat()

    for item in news_links:
        # 개별 기사에서 본문 + 작성일 수집
        article = fetch_policy_news_article(item["link"])

        news = {
            "title": item["title"],
            "link": item["link"],
            "published": article["published"],
            "source": "대한민국 정책브리핑",
            "content": article["content"],
            "collection_method": "crawling",
            "collected_at": collected_at
        }

        news_list.append(news)

    return news_list
import os
import requests
from dotenv import load_dotenv

from src.config import load_config
from src.logger import setup_logger

logger = setup_logger()


def summarize_news(news):
    """
    뉴스 1건을 AI로 분석하여 요약, 카테고리, 중요도를 추가합니다.
    """

    content = news.get("content", "")
    title = news.get("title", "")

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
        "OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요."
    )

    config = load_config()
    prompt = f"""
다음 뉴스 기사를 분석해주세요.

제목: {title}
본문: {content}

다음 형식으로만 답변해주세요.
요약: 뉴스 핵심 내용을 2~3문장으로 요약
카테고리: 정치, 경제, 사회, 국제, 문화, 스포츠, IT/과학 중 하나
중요도: 1~5 사이의 정수
"""

    response = requests.post(
    "https://copa.codyssey.kr/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}"
    },
    json={
        "model": config["ai"]["model"],
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    },
    timeout=config["request"]["timeout"],
)

    response.raise_for_status()

    response_data = response.json()

    try:
        ai_result = response_data["choices"][0]["message"]["content"]
        if not isinstance(ai_result, str) or not ai_result.strip():
            raise ValueError("AI 응답 내용이 비어 있습니다.")
    except (KeyError, IndexError, TypeError) as e:
        raise ValueError("AI 응답 형식이 올바르지 않습니다.") from e
    
    summary = ""
    category = ""
    importance = 3

    for line in ai_result.splitlines():
        line = line.strip()

        if line.startswith("요약:"):
            summary = line.replace("요약:", "", 1).strip()

        elif line.startswith("카테고리:"):
            category = line.replace("카테고리:", "", 1).strip()

        elif line.startswith("중요도:"):
            importance_text = line.replace("중요도:", "", 1).strip()
            try:
                importance = int(importance_text)
                if not 1 <= importance <= 5:
                    raise ValueError
            except ValueError:
                raise ValueError(
                    f"AI 중요도 값이 올바르지 않습니다: {importance_text}"
                )

    allowed_categories = {
        "정치", "경제", "사회", "국제",
        "문화", "스포츠", "IT/과학"
    }

    if not summary:
        raise ValueError("AI 요약문이 누락되었습니다.")

    if category not in allowed_categories:
        raise ValueError(f"AI 카테고리가 올바르지 않습니다: {category}")

    summarized_news = news.copy()

    summarized_news["summary"] = summary
    summarized_news["category"] = category
    summarized_news["importance"] = importance

    return summarized_news


def summarize_news_list(news_list):
    """
    여러 뉴스 데이터를 순서대로 AI 요약합니다.
    """

    summarized_news_list = []

    for news in news_list:
        try:
            summarized_news = summarize_news(news)
            summarized_news_list.append(summarized_news)

        except Exception as e:
            title = news.get("title", "제목 없음")
            logger.error(f"AI 요약 실패 - {title}: {e}")
            continue

    return summarized_news_list
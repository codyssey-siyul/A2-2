from collections import Counter

import os
import requests
from dotenv import load_dotenv

from src.config import load_config
from src.logger import setup_logger


logger = setup_logger()


def analyze_news(news_list):
    """
    요약된 뉴스 전체를 AI로 분석합니다.
    """

    # ------------------------------------------------------------
    # 일반 Python으로 계산하는 데이터 통계
    # 이 부분은 나중에도 그대로 사용
    # ------------------------------------------------------------

    total_news = len(news_list)

    source_counts = Counter(
        news.get("source", "알 수 없음")
        for news in news_list
    )

    category_counts = Counter(
        news.get("category", "미분류")
        for news in news_list
    )

    importance_values = [
        news.get("importance", 0)
        for news in news_list
        if isinstance(news.get("importance"), (int, float))
    ]

    if importance_values:
        average_importance = round(
            sum(importance_values) / len(importance_values),
            2
        )
    else:
        average_importance = 0

    # AI 분석에 사용할 뉴스 요약 데이터 구성
    news_text = "\n".join(
        f"- 제목: {news.get('title', '')}\n"
        f"  요약: {news.get('summary', '')}\n"
        f"  카테고리: {news.get('category', '')}"
        for news in news_list
    )

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    config = load_config()

    prompt = f"""
다음 뉴스들을 종합적으로 분석해주세요.

{news_text}

다음 형식으로만 답변해주세요.

주요이슈: 전체 뉴스에서 중요한 이슈를 2~3개로 정리
트렌드: 뉴스 전체에서 나타나는 주요 흐름을 2~3개로 정리
키워드: 핵심 키워드 5개
인사이트: 뉴스 데이터를 바탕으로 알 수 있는 시사점을 2~3개로 정리
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

    ai_result = response.json()["choices"][0]["message"]["content"]

    major_issues = []
    trends = []
    keywords = []
    insights = []

    current_section = None

    for line in ai_result.splitlines():
        line = line.strip()

        if not line:
            continue

        if line == "주요이슈:":
            current_section = "major_issues"
            continue

        elif line == "트렌드:":
            current_section = "trends"
            continue

        elif line == "키워드:":
            current_section = "keywords"
            continue

        elif line == "인사이트:":
            current_section = "insights"
            continue

        if current_section == "major_issues":
            major_issues.append(line.lstrip("- ").strip())

        elif current_section == "trends":
            trends.append(line.lstrip("- ").strip())

        elif current_section == "keywords":
            keywords.extend(
                keyword.strip().lstrip("- ").strip()
                for keyword in line.split(",")
                if keyword.strip()
            )

        elif current_section == "insights":
            insights.append(line.lstrip("- ").strip())
    
    analysis_result = {
        "total_news": total_news,
        "source_counts": dict(source_counts),
        "category_counts": dict(category_counts),
        "average_importance": average_importance,
        "major_issues": major_issues,
        "trends": trends,
        "keywords": keywords,
        "insights": insights,
    }

    return analysis_result
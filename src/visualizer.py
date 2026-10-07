from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

CHART_DIR = Path("output/charts")


def create_news_charts(news_list):
    """
    뉴스 데이터를 이용해 차트 2종을 생성합니다.

    1. 카테고리별 뉴스 건수
    2. 일별 뉴스 수집 추이
    """

    CHART_DIR.mkdir(parents=True, exist_ok=True)

    category_counts = Counter(
        news.get("category", "미분류")
        for news in news_list
    )

    plt.figure(figsize=(10, 6))

    plt.bar(
        category_counts.keys(),
        category_counts.values()
    )

    plt.title("카테고리별 뉴스 건수")
    plt.xlabel("카테고리")
    plt.ylabel("뉴스 건수")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    category_chart_path = CHART_DIR / "news_by_category.png"

    plt.savefig(category_chart_path)
    plt.close()


    daily_counts = Counter(
        news.get("collected_at", "알 수 없음")[:10]
        for news in news_list
    )

    daily_counts = dict(
        sorted(daily_counts.items())
    )

    plt.figure(figsize=(10, 6))

    plt.plot(
        daily_counts.keys(),
        daily_counts.values(),
        marker="o"
    )

    plt.title("일별 뉴스 수집 추이")
    plt.xlabel("수집일")
    plt.ylabel("뉴스 건수")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    daily_chart_path = CHART_DIR / "news_daily_trend.png"

    plt.savefig(daily_chart_path)
    plt.close()

    return {
        "category_chart": category_chart_path,
        "daily_chart": daily_chart_path,
    }
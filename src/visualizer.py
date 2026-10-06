from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

CHART_DIR = Path("output/charts")


def create_news_charts(news_list):
    """
    뉴스 데이터를 이용해 차트 2종을 생성합니다.

    현재:
    1. 출처별 뉴스 건수
    2. 게시일별 뉴스 건수

    TODO:
    OpenAI API 연결 후 실제 category가 생성되면
    2번 차트를 '카테고리별 뉴스 건수'로 교체합니다.
    """

    CHART_DIR.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------
    # 차트 1: 출처별 뉴스 건수
    # ------------------------------------------------------------

    source_counts = Counter(
        news.get("source", "알 수 없음")
        for news in news_list
    )

    plt.figure(figsize=(10, 6))

    plt.bar(
        source_counts.keys(),
        source_counts.values()
    )

    plt.title("News Count by Source")
    plt.xlabel("Source")
    plt.ylabel("News Count")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    source_chart_path = CHART_DIR / "news_by_source.png"

    plt.savefig(source_chart_path)
    plt.close()

    # ============================================================
    # [TEMP CHART START]
    #
    # 현재 Mock summarize에서는 모든 category가 "테스트"이므로
    # 임시로 게시일별 뉴스 건수를 시각화합니다.
    #
    # TODO: OpenAI API 연결 후 이 부분을
    #       '카테고리별 뉴스 건수' 차트로 교체
    # ============================================================

    published_counts = Counter(
        news.get("published", "알 수 없음")[:10]
        for news in news_list
    )

    published_counts = dict(
        sorted(published_counts.items())
    )

    plt.figure(figsize=(10, 6))

    plt.bar(
        published_counts.keys(),
        published_counts.values()
    )

    plt.title("News Count by Published Date")
    plt.xlabel("Published Date")
    plt.ylabel("News Count")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    second_chart_path = CHART_DIR / "news_by_date.png"

    plt.savefig(second_chart_path)
    plt.close()

    # ============================================================
    # [TEMP CHART END]
    # OpenAI API 연결 후 위 영역을 카테고리 차트로 교체
    # ============================================================

    return {
        "source_chart": source_chart_path,
        "second_chart": second_chart_path,
    }
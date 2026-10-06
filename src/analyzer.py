from collections import Counter


def analyze_news_mock(news_list):
    """
    요약된 뉴스 전체를 분석합니다.

    현재는 OpenAI API 없이 전체 파이프라인을 테스트하기 위한 임시 함수입니다.
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

    # ============================================================
    # [MOCK START]
    # 나중에 OpenAI API 연결 시 이 부분을 실제 AI 분석 코드로 교체
    # ============================================================

    major_issues = [
        "현재는 Mock 분석 결과입니다.",
        "실제 API 연결 후 주요 뉴스 이슈를 분석합니다."
    ]

    trends = [
        "현재는 Mock 트렌드 분석입니다.",
        "실제 API 연결 후 뉴스 전체의 흐름을 분석합니다."
    ]

    insights = [
        "현재는 Mock 인사이트입니다.",
        "실제 API 연결 후 뉴스 데이터를 기반으로 핵심 인사이트를 생성합니다."
    ]

    # ============================================================
    # [MOCK END]
    # OpenAI API 연결 시 여기까지 교체
    # ============================================================

    analysis_result = {
        "total_news": total_news,
        "source_counts": dict(source_counts),
        "category_counts": dict(category_counts),
        "average_importance": average_importance,
        "major_issues": major_issues,
        "trends": trends,
        "insights": insights,
    }

    return analysis_result
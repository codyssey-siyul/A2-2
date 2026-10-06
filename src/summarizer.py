def summarize_news_mock(news):
    """
    뉴스 1건에 Mock AI 요약 결과를 추가합니다.

    현재는 OpenAI API 없이 전체 파이프라인을 테스트하기 위한 임시 함수입니다.
    """

    content = news.get("content", "")
    title = news.get("title", "")

    # ============================================================
    # [MOCK START]
    # 나중에 OpenAI API 연결 시 이 부분을 실제 API 호출 코드로 교체
    # ============================================================

    if content:
        summary = content[:150]
    else:
        summary = f"{title} 관련 뉴스입니다."

    category = "테스트"
    importance = 3

    # ============================================================
    # [MOCK END]
    # OpenAI API 연결 시 여기까지 교체
    # ============================================================

    summarized_news = news.copy()

    summarized_news["summary"] = summary
    summarized_news["category"] = category
    summarized_news["importance"] = importance

    return summarized_news


def summarize_news_list(news_list):
    """
    여러 뉴스 데이터를 순서대로 Mock 요약합니다.
    """

    summarized_news_list = []

    for news in news_list:
        summarized_news = summarize_news_mock(news)
        summarized_news_list.append(summarized_news)

    return summarized_news_list
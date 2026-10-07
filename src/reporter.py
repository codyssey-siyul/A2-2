from pathlib import Path
import re

REQUIRED_FIELDS = [
    "title",
    "link",
    "published",
    "source",
]


def calculate_report_metrics(news_list):
    """리포트에 사용할 분석 개요와 데이터 품질 지표를 계산합니다."""

    total_news = len(news_list)

    if total_news == 0:
        return {
            "total_news": 0,
            "source_count": 0,
            "date_from": "데이터 없음",
            "date_to": "데이터 없음",
            "field_completeness": 0.0,
            "content_rate": 0.0,
            "duplicate_rate": 0.0,
        }

    # ------------------------------------------------------------
    # 분석 개요
    # ------------------------------------------------------------

    sources = {
        news.get("source")
        for news in news_list
        if news.get("source")
    }

    published_dates = [
        news.get("published", "")[:10]
        for news in news_list
        if news.get("published")
    ]

    date_from = min(published_dates) if published_dates else "알 수 없음"
    date_to = max(published_dates) if published_dates else "알 수 없음"

    # ------------------------------------------------------------
    # 품질 지표 1: 필수 필드 완전성
    # title / link / published / source가 얼마나 채워져 있는지 계산
    # ------------------------------------------------------------

    total_required_values = total_news * len(REQUIRED_FIELDS)

    valid_required_values = sum(
        1
        for news in news_list
        for field in REQUIRED_FIELDS
        if news.get(field)
    )

    field_completeness = round(
        valid_required_values / total_required_values * 100,
        2
    )

    # ------------------------------------------------------------
    # 품질 지표 2: 본문 보유율
    # content가 실제로 존재하는 뉴스 비율
    # ------------------------------------------------------------

    content_count = sum(
        1
        for news in news_list
        if news.get("content", "").strip()
    )

    content_rate = round(
        content_count / total_news * 100,
        2
    )

    # ------------------------------------------------------------
    # 품질 지표 3: 중복률
    # URL(link)을 기준으로 중복 여부 계산
    # ------------------------------------------------------------

    links = [
        news.get("link")
        for news in news_list
        if news.get("link")
    ]

    duplicate_count = len(links) - len(set(links))

    duplicate_rate = round(
        duplicate_count / total_news * 100,
        2
    )

    return {
        "total_news": total_news,
        "source_count": len(sources),
        "date_from": date_from,
        "date_to": date_to,
        "field_completeness": field_completeness,
        "content_rate": content_rate,
        "duplicate_rate": duplicate_rate,
    }

def get_top_news(news_list, top_n=5):
    """중요도 점수를 기준으로 TOP N 뉴스를 반환합니다."""

    sorted_news = sorted(
        news_list,
        key=lambda news: news.get("importance", 0),
        reverse=True
    )

    return sorted_news[:top_n]

def generate_markdown_report(news_list, analysis_result):
    """뉴스 데이터와 AI 분석 결과를 이용해 Markdown 리포트를 생성합니다."""

    metrics = calculate_report_metrics(news_list)
    top_news = get_top_news(news_list, 5)

    lines = []

    # 제목
    lines.append("# AI 뉴스 트렌드 및 종합 분석 리포트")
    lines.append("")

    # 1. 분석 개요
    lines.append("## 1. 분석 개요")
    lines.append("")
    lines.append(f"- 전체 뉴스 수: {metrics['total_news']}건")
    lines.append(
        f"- 분석 기간: {metrics['date_from']} ~ {metrics['date_to']}"
    )
    lines.append(f"- 뉴스 출처 수: {metrics['source_count']}개")
    lines.append("")

    # 2. 데이터 품질 지표
    lines.append("## 2. 데이터 품질 지표")
    lines.append("")
    lines.append(
        f"- 필수 필드 완전성: {metrics['field_completeness']}%"
    )
    lines.append(
        f"- 본문 보유율: {metrics['content_rate']}%"
    )
    lines.append(
        f"- 중복률: {metrics['duplicate_rate']}%"
    )
    lines.append("")

    # 3. TOP 5 뉴스
    lines.append("## 3. 중요도 TOP 5 뉴스")
    lines.append("")

    for index, news in enumerate(top_news, start=1):
        lines.append(f"### {index}. {news.get('title', '제목 없음')}")
        lines.append("")
        lines.append(
            f"- 출처: {news.get('source', '알 수 없음')}"
        )
        lines.append(
            f"- 중요도: {news.get('importance', 0)}"
        )
        lines.append(
            f"- 요약: {news.get('summary', '요약 없음')}"
        )
        lines.append("")

    # 4. AI 인사이트 분석
    lines.append("## 4. AI 인사이트 분석")
    lines.append("")

    lines.append("### 주요 이슈")
    lines.append("")
    for item in analysis_result.get("major_issues", []):
        lines.append(f"- {re.sub(r'^\d+[\)\.]\s*', '', item)}")
    lines.append("")

    lines.append("### 주요 트렌드")
    lines.append("")
    for item in analysis_result.get("trends", []):
        lines.append(f"- {re.sub(r'^\d+[\)\.]\s*', '', item)}")
    lines.append("")

    lines.append("### 핵심 키워드")
    lines.append("")
    for keyword in analysis_result.get("keywords", []):
        lines.append(f"- {keyword}")
    lines.append("")

    lines.append("### 시사점")
    lines.append("")
    for item in analysis_result.get("insights", []):
        lines.append(f"- {re.sub(r'^\d+[\)\.]\s*', '', item)}")
    lines.append("")

    # 5. 시각화
    lines.append("## 5. 시각화")
    lines.append("")

    lines.append("### 카테고리별 뉴스 건수")
    lines.append("")
    lines.append("![카테고리별 뉴스 건수](../charts/news_by_category.png)")
    lines.append("")

    lines.append("### 일별 뉴스 수집 추이")
    lines.append("")
    lines.append("![일별 뉴스 수집 추이](../charts/news_daily_trend.png)")
    lines.append("")

    return "\n".join(lines)


REPORT_DIR = Path("output/reports")


def save_markdown_report(report_text, source_file_path):
    """생성된 Markdown 리포트를 파일로 저장합니다."""

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    source_file_path = Path(source_file_path)

    # Summary 파일의 날짜/시간 정보를 리포트 파일명에 그대로 사용
    report_file_name = source_file_path.name.replace(
        "news_summary_", "news_report_"
    ).replace(
        ".jsonl", ".md"
    )

    report_file_path = REPORT_DIR / report_file_name

    with open(report_file_path, "w", encoding="utf-8") as file:
        file.write(report_text)

    return report_file_path
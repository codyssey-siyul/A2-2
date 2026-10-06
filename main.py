import argparse
import json
from pathlib import Path

from src.fetcher import fetch_rss_news
from src.storage import (
    save_raw_news,
    load_jsonl,
    save_clean_news,
    save_summary_news,
    save_analysis_result,
)
from src.cleaner import clean_news_list
from src.crawler import fetch_policy_news
from src.summarizer import summarize_news_list
from src.analyzer import analyze_news_mock
from src.visualizer import create_news_charts
from src.reporter import generate_markdown_report, save_markdown_report


def main():
    parser = argparse.ArgumentParser(
        description="AI 뉴스 트렌드 분석 데이터 파이프라인"
    )

    subparsers = parser.add_subparsers(dest="command")

    # 뉴스 수집 명령어
    fetch_parser = subparsers.add_parser(
        "fetch",
        help="뉴스 데이터를 수집합니다."
    )

    fetch_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="수집할 뉴스 개수"
    )

    # 뉴스 정제 명령어
    subparsers.add_parser(
        "clean",
        help="수집한 Raw 뉴스 데이터를 정제합니다."
    )

    # 뉴스 요약 명령어
    subparsers.add_parser(
        "summarize",
        help="정제된 뉴스 데이터를 AI 요약합니다."
    )

    # 뉴스 종합 분석 명령어
    subparsers.add_parser(
        "analyze",
        help="요약된 뉴스 데이터를 종합 분석합니다."
    )

    # 뉴스 차트 생성 명령어
    subparsers.add_parser(
        "chart",
        help="뉴스 데이터를 시각화하여 차트를 생성합니다."
    )

    # 뉴스 리포트 생성 명령어
    subparsers.add_parser(
        "report",
        help="뉴스 분석 결과를 종합하여 리포트를 생성합니다."
    )

    crawl_parser = subparsers.add_parser(
    "crawl",
    help="정책브리핑 뉴스를 웹 크롤링합니다."
)

    crawl_parser.add_argument(
    "--limit",
    type=int,
    default=5,
    help="크롤링할 뉴스 개수"
)

    args = parser.parse_args()

    # Fetch
    if args.command == "fetch":
        print(f"뉴스 수집 시작 - 최대 {args.limit}건")

        news_list = fetch_rss_news(args.limit)

        for index, news in enumerate(news_list, start=1):
            print(f"\n[{index}] {news['title']}")
            print(f"출처: {news['source']}")
            print(f"날짜: {news['published']}")
            print(f"링크: {news['link']}")

        file_path = save_raw_news(news_list)

        print(f"\n수집 완료: {len(news_list)}건")
        print(f"Raw 데이터 저장 완료: {file_path}")

    # Clean
    elif args.command == "clean":
        raw_files = list(
            Path("data/raw").glob("news_raw_*.jsonl")
        )

        if not raw_files:
            print("정제할 Raw 데이터가 없습니다.")
            return

        # 모든 Raw 파일을 하나의 목록으로 통합
        raw_news_list = []

        for raw_file in raw_files:
            news_list = load_jsonl(raw_file)
            raw_news_list.extend(news_list)

        # 통합된 Raw 데이터 정제 + URL 기준 중복 제거
        cleaned_news_list = clean_news_list(raw_news_list)

        # 가장 최근 Raw 파일명을 기준으로 Clean 파일 생성
        latest_raw_file = max(
            raw_files,
            key=lambda path: path.stat().st_mtime
        )
        

        clean_file_path = save_clean_news(
            cleaned_news_list,
            latest_raw_file
        )

        print(f"Raw 파일: {len(raw_files)}개")
        print(f"Raw 데이터: {len(raw_news_list)}건")
        print(f"Clean 데이터: {len(cleaned_news_list)}건")
        print(f"Clean 데이터 저장 완료: {clean_file_path}")

    # Summarize
    elif args.command == "summarize":
        clean_files = list(
            Path("data/clean").glob("news_clean_*.jsonl")
        )

        if not clean_files:
            print("요약할 Clean 데이터가 없습니다.")
            return

        # 파일명에 포함된 날짜/시간을 기준으로 가장 최근 Clean 파일 선택
        latest_clean_file = max(
            clean_files,
            key=lambda path: path.name
        )

        clean_news_list = load_jsonl(latest_clean_file)

        # 현재는 Mock 요약 사용
        # TODO: OpenAI API 연결 시 summarizer.py의 Mock 부분을 실제 API 호출로 교체
        summarized_news_list = summarize_news_list(
            clean_news_list
        )

        summary_file_path = save_summary_news(
            summarized_news_list,
            latest_clean_file
        )

        print(f"요약 대상 파일: {latest_clean_file}")
        print(f"요약 대상 뉴스: {len(clean_news_list)}건")
        print(f"요약 완료: {len(summarized_news_list)}건")
        print(f"Summary 데이터 저장 완료: {summary_file_path}")

    # Analyze
    elif args.command == "analyze":
        summary_files = list(
            Path("data/summary").glob("news_summary_*.jsonl")
        )

        if not summary_files:
            print("분석할 Summary 데이터가 없습니다.")
            return

        # 파일명에 포함된 날짜/시간을 기준으로 가장 최근 Summary 파일 선택
        latest_summary_file = max(
            summary_files,
            key=lambda path: path.name
        )

        summarized_news_list = load_jsonl(
            latest_summary_file
        )

        # 현재는 Mock AI 분석 사용
        # TODO: OpenAI API 연결 시 analyzer.py의 Mock 부분을 실제 API 호출로 교체
        analysis_result = analyze_news_mock(
            summarized_news_list
        )

        analysis_file_path = save_analysis_result(
            analysis_result,
            latest_summary_file
        )

        print(f"분석 대상 파일: {latest_summary_file}")
        print(f"분석 대상 뉴스: {len(summarized_news_list)}건")
        print(f"평균 중요도: {analysis_result['average_importance']}")
        print(f"종합 분석 완료")
        print(f"Analysis 데이터 저장 완료: {analysis_file_path}")

    # Chart
    elif args.command == "chart":
        summary_files = list(
            Path("data/summary").glob("news_summary_*.jsonl")
        )

        if not summary_files:
            print("차트를 생성할 Summary 데이터가 없습니다.")
            return

        # 파일명에 포함된 날짜/시간을 기준으로 가장 최근 Summary 파일 선택
        latest_summary_file = max(
            summary_files,
            key=lambda path: path.name
        )

        summarized_news_list = load_jsonl(
            latest_summary_file
        )

        chart_paths = create_news_charts(
            summarized_news_list
        )

        print(f"차트 대상 파일: {latest_summary_file}")
        print(f"차트 대상 뉴스: {len(summarized_news_list)}건")
        print(f"출처별 차트 저장 완료: {chart_paths['source_chart']}")
        print(f"두 번째 차트 저장 완료: {chart_paths['second_chart']}")

    # Report
    elif args.command == "report":
        summary_files = list(
            Path("data/summary").glob("news_summary_*.jsonl")
        )

        analysis_files = list(
            Path("data/analysis").glob("news_analysis_*.json")
        )

        if not summary_files:
            print("리포트를 생성할 Summary 데이터가 없습니다.")
            return

        if not analysis_files:
            print("리포트를 생성할 Analysis 데이터가 없습니다.")
            return

        # 파일명 기준으로 가장 최근 Summary / Analysis 파일 선택
        latest_summary_file = max(
            summary_files,
            key=lambda path: path.name
        )

        latest_analysis_file = max(
            analysis_files,
            key=lambda path: path.name
        )

        # Summary 데이터 로드
        summarized_news_list = load_jsonl(
            latest_summary_file
        )

        # Analysis JSON 로드
        with open(
            latest_analysis_file,
            "r",
            encoding="utf-8"
        ) as file:
            analysis_result = json.load(file)

        # Markdown 리포트 생성
        report_text = generate_markdown_report(
            summarized_news_list,
            analysis_result
        )

        # Markdown 파일 저장
        report_file_path = save_markdown_report(
            report_text,
            latest_summary_file
        )

        # 과제 요구사항: 콘솔 출력
        print("\n" + "=" * 60)
        print(report_text)
        print("=" * 60)

        print(f"\n리포트 생성 완료: {report_file_path}")

    elif args.command == "crawl":
        print(f"웹 크롤링 시작 - 최대 {args.limit}건")

        news_list = fetch_policy_news(args.limit)

        for index, news in enumerate(news_list, start=1):
            print(f"\n[{index}] {news['title']}")
            print(f"출처: {news['source']}")
            print(f"작성일: {news['published']}")
            print(f"본문 길이: {len(news['content'])}자")
            print(f"링크: {news['link']}")

        file_path = save_raw_news(news_list)

        print(f"\n크롤링 완료: {len(news_list)}건")
        print(f"Raw 데이터 저장 완료: {file_path}")

if __name__ == "__main__":
    main()
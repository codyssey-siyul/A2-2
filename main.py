import argparse
from pathlib import Path

from src.fetcher import fetch_rss_news
from src.storage import save_raw_news, load_jsonl, save_clean_news
from src.cleaner import clean_news_list
from src.crawler import fetch_policy_news


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
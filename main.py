import argparse
from pathlib import Path

from src.fetcher import fetch_rss_news
from src.storage import save_raw_news, load_jsonl, save_clean_news
from src.cleaner import clean_news_list


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

        latest_raw_file = max(
            raw_files,
            key=lambda path: path.stat().st_mtime
        )

        raw_news_list = load_jsonl(latest_raw_file)
        cleaned_news_list = clean_news_list(raw_news_list)

        clean_file_path = save_clean_news(
            cleaned_news_list,
            latest_raw_file
        )

        print(f"Raw 데이터: {len(raw_news_list)}건")
        print(f"Clean 데이터: {len(cleaned_news_list)}건")
        print(f"Clean 데이터 저장 완료: {clean_file_path}")


if __name__ == "__main__":
    main()
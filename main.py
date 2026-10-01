import argparse
from src.fetcher import fetch_rss_news
from src.storage import save_raw_news


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

    args = parser.parse_args()


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


if __name__ == "__main__":
    main()
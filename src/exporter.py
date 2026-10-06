import csv
import json
from pathlib import Path


EXPORT_DIR = Path("output/exports")


def export_news_data(news_list, source_file_path):
    """뉴스 데이터를 CSV와 JSONL 형식으로 내보냅니다."""

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    source_file_path = Path(source_file_path)

    # Summary 파일의 날짜/시간 정보를 Export 파일명에 그대로 사용
    base_name = source_file_path.stem.replace(
        "news_summary_",
        "news_export_"
    )

    csv_file_path = EXPORT_DIR / f"{base_name}.csv"
    jsonl_file_path = EXPORT_DIR / f"{base_name}.jsonl"

    # ------------------------------------------------------------
    # CSV 저장
    # ------------------------------------------------------------

    if news_list:
        # 뉴스 데이터에 존재하는 모든 필드를 자동으로 수집
        fieldnames = []

        for news in news_list:
            for key in news.keys():
                if key not in fieldnames:
                    fieldnames.append(key)

        with open(
            csv_file_path,
            "w",
            encoding="utf-8-sig",
            newline=""
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(news_list)

    # ------------------------------------------------------------
    # JSONL 저장
    # ------------------------------------------------------------

    with open(
        jsonl_file_path,
        "w",
        encoding="utf-8"
    ) as file:
        for news in news_list:
            file.write(
                json.dumps(
                    news,
                    ensure_ascii=False
                ) + "\n"
            )

    return {
        "csv": csv_file_path,
        "jsonl": jsonl_file_path,
    }
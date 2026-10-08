
import csv
import json
from pathlib import Path


EXPORT_DIR = Path("output/exports")


def export_news_data(news_list, source_file_path, export_format="all"):
    """뉴스 데이터를 선택한 형식(CSV, JSONL)으로 내보냅니다."""

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    source_file_path = Path(source_file_path)

    base_name = source_file_path.stem.replace(
        "news_summary_",
        "news_export_"
    )

    csv_file_path = EXPORT_DIR / f"{base_name}.csv"
    jsonl_file_path = EXPORT_DIR / f"{base_name}.jsonl"

    result = {}

    # CSV 저장
    if export_format in ("csv", "all"):
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
            if fieldnames:
                writer = csv.DictWriter(
                    file,
                    fieldnames=fieldnames
                )
                writer.writeheader()
                writer.writerows(news_list)

        result["csv"] = csv_file_path

    # JSONL 저장
    if export_format in ("jsonl", "all"):
        with open(
            jsonl_file_path,
            "w",
            encoding="utf-8"
        ) as file:
            for news in news_list:
                file.write(
                    json.dumps(news, ensure_ascii=False) + "\n"
                )

        result["jsonl"] = jsonl_file_path

    return result

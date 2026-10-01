import json
from datetime import datetime, timezone
from pathlib import Path


RAW_DATA_DIR = Path("data/raw")


def save_raw_news(news_list):
    """수집한 뉴스 데이터를 Raw JSONL 파일로 저장합니다."""

    # data/raw 폴더가 없으면 자동 생성
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 실행할 때마다 파일 이름에 수집 시각을 기록
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = RAW_DATA_DIR / f"news_raw_{timestamp}.jsonl"

    collected_at = datetime.now(timezone.utc).isoformat()

    with open(file_path, "w", encoding="utf-8") as file:
        for news in news_list:
            raw_news = news.copy()
            raw_news["collected_at"] = collected_at

            file.write(
                json.dumps(raw_news, ensure_ascii=False) + "\n"
            )

    return file_path

def load_jsonl(file_path):
    """JSONL 파일을 읽어 뉴스 목록으로 반환합니다."""

    news_list = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            news_list.append(json.loads(line))

    return news_list


def save_clean_news(news_list, source_file_path):
    """정제된 뉴스 데이터를 Clean JSONL 파일로 저장합니다."""

    clean_data_dir = Path("data/clean")
    clean_data_dir.mkdir(parents=True, exist_ok=True)

    source_file_path = Path(source_file_path)

    # Raw 파일 이름의 시간 정보를 그대로 사용
    clean_file_name = source_file_path.name.replace(
        "news_raw_", "news_clean_"
    )

    clean_file_path = clean_data_dir / clean_file_name

    with open(clean_file_path, "w", encoding="utf-8") as file:
        for news in news_list:
            file.write(
                json.dumps(news, ensure_ascii=False) + "\n"
            )

    return clean_file_path
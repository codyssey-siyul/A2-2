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
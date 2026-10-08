# AI 기반 뉴스 수집 및 트렌드 분석 CLI

## 1. 프로젝트 소개

뉴스 데이터를 수집하고 AI를 활용해 주요 내용을 요약·분석하는 Python 기반 CLI(Command Line Interface) 프로젝트입니다.

RSS 및 웹 크롤링을 통해 뉴스를 수집하고, 데이터를 정제한 뒤 AI 요약, 트렌드 분석, 시각화, Markdown 보고서 생성까지 수행합니다.

### 주요 목표

- 뉴스 수집 및 데이터 정제 자동화
- AI를 활용한 뉴스 요약과 중요도 분류
- 주요 이슈, 트렌드 및 인사이트 도출
- 분석 결과 시각화 및 보고서 생성
- CSV, JSONL 형식으로 데이터 내보내기

## 2. 주요 기능

| 기능 | 설명 |
|---|---|
| RSS 수집 | RSS 피드를 이용한 뉴스 수집 |
| 웹 크롤링 | 웹페이지 기반 뉴스 콘텐츠 수집 |
| 데이터 정제 | 날짜 형식 통일, 필수 항목 검증, 중복 제거 |
| AI 요약 | 뉴스 요약, 카테고리 분류, 중요도 평가 |
| AI 분석 | 주요 이슈, 트렌드, 키워드 및 인사이트 도출 |
| 시각화 | 카테고리별 뉴스 분포, 일별 뉴스 추이 |
| 보고서 | Markdown 형식의 분석 보고서 생성 |
| 데이터 내보내기 | CSV 및 JSONL 형식 지원 |
| 로깅 | 작업 진행 상태 및 오류 기록 |

## 3. 개발 환경

- Python 3.14
- Visual Studio Code
- Python 가상환경 (`venv`)
- PowerShell
- Codyssey AI API
- Git / GitHub

주요 Python 패키지는 `requirements.txt`에서 관리합니다.

## 4. 프로젝트 구조

```text
A2-2/
├── main.py
├── config.json
├── requirements.txt
├── .gitignore
├── .env
├── README.md
├── src/
│   ├── fetcher.py
│   ├── crawler.py
│   ├── cleaner.py
│   ├── summarizer.py
│   ├── analyzer.py
│   ├── visualizer.py
│   ├── reporter.py
│   ├── exporter.py
│   ├── storage.py
│   ├── config.py
│   └── logger.py
├── data/
│   ├── raw/
│   ├── clean/
│   ├── summary/
│   └── analysis/
└── output/
    ├── charts/
    └── reports/
```

`.env`와 `.venv`는 로컬 실행 환경에서 사용하는 파일 및 폴더이며, API 키가 포함된 `.env`는 GitHub에 업로드하지 않습니다.

## 5. 설치 및 실행 방법

### 5.1 프로젝트 다운로드

```bash
git clone https://github.com/codyssey-siyul/A2-2.git
cd A2-2
```

### 5.2 가상환경 생성

```powershell
python -m venv .venv
```

Windows PowerShell에서 가상환경 활성화:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5.3 라이브러리 설치

```powershell
pip install -r requirements.txt
```

### 5.4 환경변수 설정

프로젝트 최상위 폴더에 `.env` 파일을 생성하고 발급받은 API 키를 입력합니다.

```env
OPENAI_API_KEY=발급받은_API_키
```

실제 API 키는 소스코드나 GitHub에 공개하지 않습니다.

## 6. CLI 사용법

기본 명령어:

```powershell
python main.py --help
```

### 6.1 RSS 뉴스 수집

```powershell
python main.py fetch --limit 5
```

### 6.2 웹 크롤링

```powershell
python main.py crawl --limit 5
```

### 6.3 데이터 정제

```powershell
python main.py clean
```

### 6.4 AI 뉴스 요약

```powershell
python main.py summarize --unsummarized
```

이미 요약된 뉴스의 중복 API 호출을 방지할 수 있습니다.

### 6.5 AI 트렌드 분석

```powershell
python main.py analyze
```

날짜나 카테고리 조건을 적용할 수도 있습니다.

```powershell
python main.py analyze --date 2026-10-01
```

### 6.6 차트 생성

```powershell
python main.py chart
```

생성되는 차트:

- `output/charts/news_by_category.png`
- `output/charts/news_daily_trend.png`

### 6.7 Markdown 보고서 생성

```powershell
python main.py report
```

보고서는 `output/reports/`에 저장됩니다.

### 6.8 데이터 내보내기

```powershell
python main.py export
```

CSV 형식만 내보내기:

```powershell
python main.py export --format csv
```

JSONL 형식만 내보내기:

```powershell
python main.py export --format jsonl
```

요약 완료된 뉴스만 CSV로 내보내기:

```powershell
python main.py export --status summarized --format csv
```

## 7. 데이터 처리 흐름

```text
RSS / 웹 크롤링
       ↓
Raw 뉴스 저장
       ↓
데이터 정제 및 중복 제거
       ↓
Clean 뉴스 저장
       ↓
AI 요약 / 분류 / 중요도 평가
       ↓
AI 트렌드 분석
       ↓
차트 생성 및 보고서 작성
       ↓
CSV / JSONL 내보내기
```

각 단계의 결과를 파일로 저장하여 후속 처리에 활용합니다.

## 8. 실행 및 테스트 결과

2026년 10월 8일 기준 기능 테스트를 수행했습니다.

| 테스트 항목 | 결과 |
|---|---|
| RSS 뉴스 수집 | 정상 |
| 웹 크롤링 | 정상 |
| 뉴스 정제 및 중복 제거 | 정상 |
| AI 뉴스 요약 | 정상 |
| AI 트렌드 분석 | 정상 |
| 카테고리별 차트 생성 | 정상 |
| 일별 뉴스 추이 차트 생성 | 정상 |
| Markdown 보고서 생성 | 정상 |
| CSV / JSONL 내보내기 | 정상 |
| 중복 AI 요약 방지 | 정상 |
| CLI 옵션 및 입력값 검증 | 정상 |

테스트 과정에서 총 16건의 정제된 뉴스에 대해 AI 요약과 분석을 수행했습니다.

분석 결과를 바탕으로 주요 이슈, 트렌드, 키워드 및 인사이트를 포함하는 보고서를 생성했습니다.

## 9. 프로젝트 특징

- 기능별 모듈 분리로 유지보수 용이
- CLI 옵션을 통한 수집 및 분석 조건 설정
- JSONL 기반 단계별 데이터 저장
- AI 요약 결과의 중복 처리 방지
- 데이터 품질 지표를 포함한 보고서 생성
- 한국어 시각화 지원
- API 키의 환경변수 분리
- 실행 로그 및 예외 처리

## 10. 향후 개선 방향

- 뉴스 수집 채널 확대
- AI 요약 및 카테고리 분류 정확도 개선
- 분석 기간별 트렌드 비교 기능 강화
- 자동 실행 및 정기 보고서 생성
- 웹 기반 대시보드 연동

---

본 프로젝트는 Python 기반 데이터 파이프라인과 AI 분석 기능을 CLI 환경에서 구현하는 것을 목표로 개발했습니다.
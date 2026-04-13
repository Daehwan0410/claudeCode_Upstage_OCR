# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

AI 영수증 지출 관리 시스템 — 영수증 이미지(JPG/PNG) 또는 PDF를 업로드하면 **Upstage Vision LLM**이 OCR로 항목을 추출하고, FastAPI 백엔드가 SQLite에 저장하며, React 프론트엔드에서 Recharts로 지출 통계를 시각화하는 웹 앱이다.

---

## 저장소 구조 (목표 상태)

```
/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI 진입점, CORS 설정
│   │   ├── api/                 # 라우터: receipts.py, stats.py, categories.py
│   │   ├── core/                # config.py (환경변수), database.py (SQLAlchemy 엔진)
│   │   ├── models/              # SQLAlchemy ORM 모델 (receipts, receipt_items)
│   │   ├── schemas/             # Pydantic 스키마 (요청/응답 검증)
│   │   └── services/
│   │       └── ocr_service.py   # LangChain + Upstage Vision LLM 연동 핵심 로직
│   ├── uploads/                 # 업로드 이미지 런타임 저장 경로
│   ├── .env                     # UPSTAGE_API_KEY, DATABASE_URL, UPLOAD_DIR
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/               # Dashboard, Upload, ReceiptList, ReceiptDetail, Stats
│   │   ├── components/          # common/(Navbar, Toast), charts/, receipt/
│   │   └── api/client.js        # Axios 인스턴스 + API 함수 모음
│   ├── .env                     # VITE_API_BASE_URL
│   └── package.json
└── images/                      # 개발용 샘플 영수증 이미지 (테스트 전용)
```

---

## 개발 환경 설정

### 백엔드

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

- API 문서: http://localhost:8000/docs
- `.env`에 `UPSTAGE_API_KEY` 설정 필수

### 프론트엔드

```bash
cd frontend
npm install
npm run dev       # 개발 서버 (기본 포트 5173)
npm run build     # Vercel 배포용 프로덕션 빌드
npm run lint      # ESLint 실행
```

---

## 핵심 아키텍처

### 데이터 흐름

```
브라우저(React) → POST /api/receipts/upload (multipart)
  → FastAPI → ocr_service.py
    → LangChain ChatUpstage (Vision LLM)
      → 구조화 JSON 반환
  → SQLAlchemy → SQLite (receipts + receipt_items)
  → 응답: 저장된 영수증 전체 정보

브라우저 → GET /api/stats/summary?start_date=&end_date=
  → FastAPI → SQLite 집계 쿼리
  → Recharts BarChart / PieChart / LineChart 렌더링
```

### OCR 서비스 (`ocr_service.py`)

Upstage Vision LLM을 LangChain으로 호출하여 아래 JSON을 반환하도록 프롬프트를 구성한다:

```json
{
  "date": "YYYY-MM-DD",
  "store_name": "상호명",
  "items": [{ "name": "상품명", "quantity": 1, "price": 0 }],
  "total": 0,
  "category": "식료품 | 외식 | 쇼핑 | 교통 | 의료 | 교육 | 문화·여가 | 기타"
}
```

OCR 실패 또는 필드 누락 시 `raw_json` 컬럼에 원본을 보관하고 수동 수정 UI로 안내한다.

### DB 모델

- `receipts` — 영수증 헤더 (store_name, date, total_amount, category, image_path, raw_json)
- `receipt_items` — 개별 항목 (receipt_id FK + CASCADE DELETE, item_name, quantity, unit_price, total_price)

### API 엔드포인트 요약

| Method | URL | 설명 |
|--------|-----|------|
| POST | `/api/receipts/upload` | 파일 업로드 + OCR + 저장 |
| GET | `/api/receipts` | 목록 조회 (page, size, start_date, end_date, category, store_name) |
| GET | `/api/receipts/{id}` | 상세 조회 |
| PUT | `/api/receipts/{id}` | 수정 |
| DELETE | `/api/receipts/{id}` | 삭제 (CASCADE) |
| GET | `/api/stats/summary` | 기간별·카테고리별 통계 |
| GET | `/api/categories` | 카테고리 목록 |

---

## 환경 변수

| 변수명 | 위치 | 설명 |
|--------|------|------|
| `UPSTAGE_API_KEY` | `backend/.env` | Upstage API 인증 키 (필수) |
| `DATABASE_URL` | `backend/.env` | 기본값: `sqlite:///./receipts.db` |
| `UPLOAD_DIR` | `backend/.env` | 기본값: `./uploads` |
| `VITE_API_BASE_URL` | `frontend/.env` | 백엔드 URL (예: `http://localhost:8000`) |

`.env` 파일은 절대 git에 커밋하지 않는다. `.gitignore`에 반드시 포함할 것.

---

## 파일 업로드 제약

- 허용 MIME 타입: `image/jpeg`, `image/png`, `application/pdf`
- 최대 크기: 10MB
- 클라이언트 사이드 검증 + 서버 사이드 검증 이중 적용

## 샘플 이미지

`images/` 디렉토리에 실제 영수증 샘플이 있다. OCR 기능 개발·테스트 시 활용한다.

| 파일명 | 영수증 종류 |
|--------|-----------|
| `01_emart.png` | 이마트 (식료품) |
| `02_starbucks.png` | 스타벅스 (외식) |
| `03_cu.jpg` | CU 편의점 |
| `03_lotte_depart.png` | 롯데백화점 (쇼핑) |
| `04_lotteria.png` | 롯데리아 (외식) |
| `05_ikea.png` | 이케아 (쇼핑) |
| `07_cgv.png` | CGV (문화·여가) |
| `09_medical.png` | 의원 (의료) |
| `11_taxi.png` | 택시 (교통) |
| `GS25편의점_영수증.pdf` | GS25 (PDF 형식) |

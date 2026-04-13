import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import create_tables
from app.api import receipts, stats, categories


@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 시작 시 DB 테이블 생성 및 업로드 디렉토리 초기화."""
    create_tables()
    os.makedirs(settings.upload_dir, exist_ok=True)
    yield


app = FastAPI(
    title="AI 영수증 지출 관리 시스템",
    description="Upstage Vision LLM 기반 영수증 OCR 및 지출 관리 API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 업로드 파일 정적 서빙 (/uploads/파일명 으로 접근)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

# 라우터 등록
app.include_router(receipts.router, prefix="/api/receipts", tags=["영수증"])
app.include_router(stats.router, prefix="/api/stats", tags=["통계"])
app.include_router(categories.router, prefix="/api", tags=["카테고리"])


@app.get("/health", tags=["헬스체크"])
def health_check():
    return {"status": "ok", "version": "1.0.0"}

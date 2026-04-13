from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # Upstage API
    upstage_api_key: str = ""

    # 데이터베이스
    database_url: str = "sqlite:///./receipts.db"

    # 파일 업로드
    upload_dir: str = "./uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_mime_types: List[str] = ["image/jpeg", "image/png", "application/pdf"]

    # CORS — 로컬 + 배포 환경
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    # Vercel 프리뷰·프로덕션 URL 전체 허용 (*.vercel.app)
    # 커스텀 도메인 사용 시 CORS_ORIGINS 환경변수에 추가
    cors_origin_regex: str = r"https://.*\.vercel\.app"


settings = Settings()

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

    # CORS
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]


settings = Settings()

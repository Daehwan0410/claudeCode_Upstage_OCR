from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  # SQLite 멀티스레드 허용
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def create_tables() -> None:
    """앱 시작 시 DB 테이블을 자동 생성한다."""
    from app.models import receipt  # noqa: F401 — ORM 모델을 Base에 등록
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI Depends로 주입하는 DB 세션 제공자."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

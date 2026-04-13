from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.receipt import StatsSummaryResponse

router = APIRouter()


@router.get("/summary", response_model=StatsSummaryResponse)
def get_stats_summary(
    start_date: str = Query(..., description="조회 시작일 (YYYY-MM-DD)"),
    end_date: str = Query(..., description="조회 종료일 (YYYY-MM-DD)"),
    group_by: str = Query(default="month", pattern="^(day|month)$"),
    db: Session = Depends(get_db),
):
    """
    기간별·카테고리별 지출 통계를 반환한다.
    TODO: Week 4 — SQLAlchemy 집계 쿼리 구현
    """
    return StatsSummaryResponse(
        total_amount=0,
        by_category=[],
        by_period=[],
    )

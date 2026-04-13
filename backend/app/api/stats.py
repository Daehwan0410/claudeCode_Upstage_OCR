from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.schemas.receipt import StatsSummaryResponse

router = APIRouter()


@router.get(
    "/summary",
    response_model=StatsSummaryResponse,
    summary="지출 통계 조회",
    response_description="기간별·카테고리별 지출 집계 데이터",
)
def get_stats_summary(
    start_date: Optional[str] = Query(default=None, description="조회 시작일 (YYYY-MM-DD). 미입력 시 전체 기간"),
    end_date: Optional[str] = Query(default=None, description="조회 종료일 (YYYY-MM-DD). 미입력 시 전체 기간"),
    db: Session = Depends(get_db),
):
    """
    선택한 기간의 지출 통계를 반환합니다.

    - **total_amount**: 기간 내 총 지출 합계
    - **by_category**: 카테고리별 지출 금액과 비율(%)
    - **by_period**: 월별 지출 합계 (Recharts BarChart·LineChart용)

    날짜 미입력 시 전체 기간 통계를 반환합니다.

    > ⚙️ SQLAlchemy 집계 쿼리는 **2주차**에 구현됩니다.
    """
    return StatsSummaryResponse(
        total_amount=0.0,
        by_category=[],
        by_period=[],
    )

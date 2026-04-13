from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

CATEGORIES: list[str] = [
    "식료품",
    "외식",
    "쇼핑",
    "교통",
    "의료",
    "교육",
    "문화·여가",
    "기타",
]


class CategoryListResponse(BaseModel):
    categories: list[str]


@router.get(
    "/categories",
    response_model=CategoryListResponse,
    summary="카테고리 목록 조회",
    response_description="지출 카테고리 전체 목록",
)
def get_categories() -> CategoryListResponse:
    """
    영수증 분류에 사용되는 카테고리 목록을 반환합니다.

    OCR 분석 및 수동 수정 화면의 카테고리 드롭다운에 사용됩니다.
    """
    return CategoryListResponse(categories=CATEGORIES)

from fastapi import APIRouter

router = APIRouter()

CATEGORIES = ["식료품", "외식", "쇼핑", "교통", "의료", "교육", "문화·여가", "기타"]


@router.get("/categories")
def get_categories() -> dict:
    return {"categories": CATEGORIES}

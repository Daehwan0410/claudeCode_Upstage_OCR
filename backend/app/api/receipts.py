from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.schemas.receipt import (
    ReceiptResponse,
    ReceiptListResponse,
    ReceiptUpdate,
)

router = APIRouter()


@router.post(
    "/upload",
    response_model=ReceiptResponse,
    status_code=201,
    summary="영수증 업로드 및 OCR 분석",
    response_description="OCR로 추출된 영수증 정보 및 저장된 DB 레코드",
)
async def upload_receipt(
    file: UploadFile = File(..., description="JPG, PNG, PDF (최대 10MB)"),
    db: Session = Depends(get_db),
):
    """
    영수증 이미지(JPG/PNG) 또는 PDF를 업로드합니다.

    - **OCR 분석**: Upstage Vision LLM이 날짜·상호명·항목·금액을 자동 추출
    - **DB 저장**: 추출 결과를 receipts + receipt_items 테이블에 저장
    - **파일 제약**: 허용 MIME — image/jpeg, image/png, application/pdf / 최대 10MB

    > ⚙️ OCR 서비스는 **2주차**에 구현됩니다.
    """
    raise HTTPException(status_code=501, detail="OCR 서비스 구현 예정 (2주차)")


@router.get(
    "",
    response_model=ReceiptListResponse,
    summary="영수증 목록 조회",
    response_description="필터·검색·페이지네이션이 적용된 영수증 목록",
)
def list_receipts(
    page: int = Query(default=1, ge=1, description="페이지 번호 (1부터 시작)"),
    size: int = Query(default=20, ge=1, le=100, description="페이지당 건수 (최대 100)"),
    start_date: Optional[str] = Query(default=None, description="조회 시작일 (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(default=None, description="조회 종료일 (YYYY-MM-DD)"),
    category: Optional[str] = Query(default=None, description="카테고리 필터 (예: 외식, 쇼핑)"),
    keyword: Optional[str] = Query(default=None, description="상호명 키워드 검색 (부분 일치)"),
    db: Session = Depends(get_db),
):
    """
    저장된 영수증 목록을 최신순으로 조회합니다.

    - **날짜 필터**: `start_date` ~ `end_date` 범위 내 영수증만 반환
    - **카테고리 필터**: 정확히 일치하는 카테고리만 반환
    - **키워드 검색**: 상호명 부분 일치 검색 (대소문자 무시)
    - **페이지네이션**: `page` + `size` 조합으로 분할 조회

    > ⚙️ 필터·페이지네이션 로직은 **2주차**에 구현됩니다.
    """
    return ReceiptListResponse(total=0, page=page, size=size, items=[])


@router.get(
    "/{receipt_id}",
    response_model=ReceiptResponse,
    summary="영수증 상세 조회",
    response_description="영수증 헤더 + 개별 항목 목록",
)
def get_receipt(
    receipt_id: int,
    db: Session = Depends(get_db),
):
    """
    특정 영수증의 상세 정보와 개별 항목(receipt_items)을 조회합니다.

    - 존재하지 않는 ID는 **404** 반환

    > ⚙️ 2주차에 구현됩니다.
    """
    raise HTTPException(status_code=404, detail="영수증을 찾을 수 없습니다")


@router.put(
    "/{receipt_id}",
    response_model=ReceiptResponse,
    summary="영수증 수정",
    response_description="수정이 반영된 영수증 전체 정보",
)
def update_receipt(
    receipt_id: int,
    body: ReceiptUpdate,
    db: Session = Depends(get_db),
):
    """
    AI가 추출한 영수증 정보(상호명·날짜·카테고리·항목)를 수동으로 수정합니다.

    - `items`를 전달하면 기존 항목을 **전체 교체**(삭제 후 재삽입)
    - `items`를 생략하면 헤더 정보만 업데이트
    - 존재하지 않는 ID는 **404** 반환

    > ⚙️ 2주차에 구현됩니다.
    """
    raise HTTPException(status_code=404, detail="영수증을 찾을 수 없습니다")


@router.delete(
    "/{receipt_id}",
    status_code=204,
    summary="영수증 삭제",
)
def delete_receipt(
    receipt_id: int,
    db: Session = Depends(get_db),
):
    """
    영수증과 연결된 모든 항목(receipt_items)을 삭제합니다.

    - ON DELETE CASCADE로 항목 자동 삭제
    - 업로드 이미지 파일도 함께 삭제
    - 존재하지 않는 ID는 **404** 반환
    - 성공 시 **204 No Content** 반환

    > ⚙️ 2주차에 구현됩니다.
    """
    raise HTTPException(status_code=404, detail="영수증을 찾을 수 없습니다")

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


@router.post("/upload", response_model=ReceiptResponse, status_code=201)
async def upload_receipt(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    영수증 이미지(JPG/PNG) 또는 PDF를 업로드하여 OCR 분석 후 DB에 저장한다.
    TODO: Week 2 — ocr_service.py 구현 후 연동
    """
    raise HTTPException(status_code=501, detail="OCR 서비스 구현 예정 (2주차)")


@router.get("", response_model=ReceiptListResponse)
def list_receipts(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    start_date: Optional[str] = Query(default=None, description="YYYY-MM-DD"),
    end_date: Optional[str] = Query(default=None, description="YYYY-MM-DD"),
    category: Optional[str] = Query(default=None),
    store_name: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    """
    저장된 영수증 목록을 조회한다. 날짜·카테고리·상호명 필터 지원.
    TODO: Week 2 — 필터링 + 페이지네이션 구현
    """
    return ReceiptListResponse(total=0, page=page, size=size, items=[])


@router.get("/{receipt_id}", response_model=ReceiptResponse)
def get_receipt(receipt_id: int, db: Session = Depends(get_db)):
    """특정 영수증 상세 정보 및 항목을 조회한다. TODO: Week 2"""
    raise HTTPException(status_code=404, detail="영수증을 찾을 수 없습니다")


@router.put("/{receipt_id}", response_model=ReceiptResponse)
def update_receipt(
    receipt_id: int,
    body: ReceiptUpdate,
    db: Session = Depends(get_db),
):
    """영수증 정보 및 항목을 수정한다. TODO: Week 2"""
    raise HTTPException(status_code=404, detail="영수증을 찾을 수 없습니다")


@router.delete("/{receipt_id}", status_code=204)
def delete_receipt(receipt_id: int, db: Session = Depends(get_db)):
    """영수증 및 관련 항목을 삭제한다 (CASCADE). TODO: Week 2"""
    raise HTTPException(status_code=404, detail="영수증을 찾을 수 없습니다")

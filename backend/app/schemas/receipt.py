from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


# ── 항목 스키마 ────────────────────────────────────────────────────────────────

class ReceiptItemBase(BaseModel):
    item_name: str
    quantity: int = Field(default=1, ge=1)
    unit_price: float = Field(ge=0)
    total_price: float = Field(ge=0)


class ReceiptItemCreate(ReceiptItemBase):
    pass


class ReceiptItemUpdate(BaseModel):
    item_name: Optional[str] = None
    quantity: Optional[int] = Field(default=None, ge=1)
    unit_price: Optional[float] = Field(default=None, ge=0)
    total_price: Optional[float] = Field(default=None, ge=0)


class ReceiptItemResponse(ReceiptItemBase):
    id: int
    receipt_id: int

    model_config = {"from_attributes": True}


# ── 영수증 스키마 ──────────────────────────────────────────────────────────────

class ReceiptBase(BaseModel):
    store_name: str
    date: date
    total_amount: float = Field(ge=0)
    category: Optional[str] = None


class ReceiptCreate(ReceiptBase):
    items: list[ReceiptItemCreate] = []


class ReceiptUpdate(BaseModel):
    store_name: Optional[str] = None
    date: Optional[date] = None
    total_amount: Optional[float] = Field(default=None, ge=0)
    category: Optional[str] = None
    items: Optional[list[ReceiptItemCreate]] = None


class ReceiptResponse(ReceiptBase):
    id: int
    image_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    items: list[ReceiptItemResponse] = []

    model_config = {"from_attributes": True}


class ReceiptListItem(ReceiptBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ReceiptListResponse(BaseModel):
    total: int
    page: int
    size: int
    items: list[ReceiptListItem]


# ── 통계 스키마 ────────────────────────────────────────────────────────────────

class CategoryStat(BaseModel):
    category: str
    amount: float
    ratio: float


class PeriodStat(BaseModel):
    period: str
    amount: float


class StatsSummaryResponse(BaseModel):
    total_amount: float
    by_category: list[CategoryStat]
    by_period: list[PeriodStat]

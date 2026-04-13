"""
Upstage Vision LLM OCR 서비스
Week 2에서 구현 예정

구현 계획:
  1. 업로드 파일(이미지/PDF)을 base64 인코딩
  2. LangChain ChatUpstage로 Vision LLM 호출
  3. 구조화 JSON 파싱 및 반환

기대 출력 스키마:
  {
    "date": "YYYY-MM-DD",
    "store_name": "상호명",
    "items": [{"name": "상품명", "quantity": 1, "price": 0}],
    "total": 0,
    "category": "식료품 | 외식 | 쇼핑 | 교통 | 의료 | 교육 | 문화·여가 | 기타"
  }
"""
# TODO: Week 2 구현
# from langchain_upstage import ChatUpstage
# from langchain_core.messages import HumanMessage

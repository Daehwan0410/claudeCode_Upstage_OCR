#!/usr/bin/env python
"""
Upstage API 연결 테스트 스크립트 (Day 4)

실행 방법:
  cd backend
  python test_upstage_connection.py
"""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def check_api_key() -> bool:
    """① .env에 실제 API 키가 설정됐는지 확인"""
    api_key = os.getenv("UPSTAGE_API_KEY", "")
    placeholder = "여기에_Upstage_API_키_입력"

    if not api_key or api_key == placeholder:
        print("[FAIL] UPSTAGE_API_KEY가 .env에 설정되지 않았습니다.")
        print("       backend/.env 파일을 열어 실제 키로 교체하세요.")
        print("       발급: https://console.upstage.ai/")
        return False

    masked = f"{api_key[:6]}...{api_key[-4:]}"
    print(f"[ OK ] API 키 감지: {masked}")
    return True


def test_chat_connection() -> bool:
    """② ChatUpstage (Solar LLM) 텍스트 연결 테스트"""
    try:
        from langchain_upstage import ChatUpstage
        from langchain_core.messages import HumanMessage

        print("\n[ >> ] ChatUpstage 연결 테스트 중...")
        chat = ChatUpstage()
        response = chat.invoke([HumanMessage(content="한국어로 '연결 성공'이라고만 답하세요.")])
        print(f"[ OK ] Solar LLM 응답: {response.content.strip()}")
        return True
    except Exception as e:
        print(f"[FAIL] ChatUpstage 연결 실패: {e}")
        return False


def test_document_parse() -> bool:
    """③ Document Parse (OCR) 테스트 — 샘플 이미지 사용"""
    sample_dir = Path("../images")
    samples = sorted(sample_dir.glob("*.png"))

    if not samples:
        print("\n[SKIP] 샘플 이미지 없음 — Document Parse 테스트 건너뜀")
        return True

    sample_path = samples[0]
    print(f"\n[ >> ] Document Parse 테스트 중: {sample_path.name}")

    try:
        from langchain_upstage import UpstageDocumentParseLoader

        loader = UpstageDocumentParseLoader(
            str(sample_path),
            split="none",
            output_type="text",
        )
        docs = loader.load()

        if not docs:
            print("[FAIL] Document Parse 응답 없음")
            return False

        preview = docs[0].page_content[:150].replace("\n", " ")
        print(f"[ OK ] OCR 결과 (앞 150자): {preview}...")
        return True

    except Exception as e:
        print(f"[FAIL] Document Parse 실패: {e}")
        return False


def main() -> None:
    print("=" * 55)
    print("  Upstage API 연결 테스트  (Day 4)")
    print("=" * 55)

    # ① API 키 확인
    key_ok = check_api_key()
    if not key_ok:
        print("\n[STOP] API 키 미설정 - 나머지 테스트 중단")
        sys.exit(1)

    # ② ~ ③ 연결 테스트
    results = [
        ("API 키 확인", True),
        ("ChatUpstage (Solar LLM)", test_chat_connection()),
        ("Document Parse (OCR)", test_document_parse()),
    ]

    print("\n" + "=" * 55)
    print("  테스트 결과 요약")
    print("=" * 55)

    all_ok = True
    for name, passed in results:
        icon = "[ OK ]" if passed else "[FAIL]"
        print(f"  {icon}  {name}")
        if not passed:
            all_ok = False

    if all_ok:
        print("\n  모든 테스트 통과! Upstage API 연결 정상.")
        print("  Day 4 완료 - Day 5(React 라우팅 설정)로 진행하세요.")
    else:
        print("\n  일부 테스트 실패. UPSTAGE_API_KEY를 확인하세요.")

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()

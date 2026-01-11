"""경기도의회 의원 데이터 스크래핑"""
import json
import os
import re
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.ggc.go.kr"
LIST_URL = f"{BASE_URL}/site/main/memberInfo/actvMmbr/list"

# 출력 경로
OUTPUT_DIR = Path(__file__).parent
PHOTOS_DIR = Path(__file__).parent.parent.parent / "frontend" / "public" / "images" / "members"


def fetch_page(page_num: int = 1) -> str:
    """페이지 HTML 가져오기"""
    params = {
        "menu": "consonant",
        "page": page_num,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(LIST_URL, params=params, headers=headers)
    response.raise_for_status()
    return response.text


def parse_members(html: str) -> list[dict]:
    """HTML에서 의원 정보 파싱 (Playwright 스크래핑 결과 기반)"""
    soup = BeautifulSoup(html, "html.parser")
    members = []

    # 의원 목록 컨테이너 찾기
    member_list = soup.select_one(".members-search-list")
    if not member_list:
        member_list = soup

    # PhotoPath가 포함된 이미지 찾기 (의원 사진)
    images = member_list.select("img[alt]")

    for img in images:
        try:
            src = img.get("src", "")
            if "PhotoPath" not in src:
                continue

            # 이름은 alt 속성에서
            name = img.get("alt", "").strip()
            if not name:
                continue

            # 사진 URL
            photo_url = urljoin(BASE_URL, src)

            # 부모 요소에서 추가 정보 찾기
            parent = img.find_parent("li") or img.find_parent("div")
            party = ""
            district = ""
            committees = []

            if parent:
                # 모든 텍스트 요소 검색
                text_elements = parent.select("span, dd, li, p, strong")
                for elem in text_elements:
                    text = elem.get_text(strip=True)
                    if not text:
                        continue
                    # 정당
                    if text in ["더불어민주당", "국민의힘", "무소속", "개혁신당", "진보당"]:
                        party = text
                    elif "당" in text and len(text) < 10:
                        party = text
                    # 선거구
                    elif "선거구" in text:
                        district = text
                    # 위원회
                    elif "위원" in text:
                        committees.append(text)

            members.append({
                "name": name,
                "photo_url": photo_url,
                "party": party,
                "district": district,
                "committees": committees,
            })
        except Exception as e:
            print(f"[ERROR] 파싱 오류: {e}")
            continue

    return members


def download_photo(url: str, name: str) -> str:
    """사진 다운로드"""
    if not url:
        return ""

    # 파일명 생성 (한글 이름을 안전한 파일명으로)
    safe_name = re.sub(r"[^\w가-힣]", "", name)
    filename = f"{safe_name}.jpg"
    filepath = PHOTOS_DIR / filename

    if filepath.exists():
        print(f"[SKIP] 이미 존재: {filename}")
        return f"/images/members/{filename}"

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"[OK] 다운로드: {filename}")
        return f"/images/members/{filename}"
    except Exception as e:
        print(f"[ERROR] 다운로드 실패 {name}: {e}")
        return ""


def scrape_all_members() -> list[dict]:
    """모든 의원 정보 스크래핑"""
    all_members = []

    for page in range(1, 12):  # 1~11페이지
        print(f"[INFO] 페이지 {page}/11 스크래핑 중...")
        try:
            html = fetch_page(page)
            members = parse_members(html)
            all_members.extend(members)
            print(f"       {len(members)}명 발견")
            time.sleep(0.5)  # 요청 간격
        except Exception as e:
            print(f"[ERROR] 페이지 {page} 실패: {e}")

    return all_members


def save_members_json(members: list[dict], download_photos: bool = True):
    """의원 데이터 JSON 저장"""
    # 사진 다운로드
    if download_photos:
        print("\n[INFO] 사진 다운로드 시작...")
        for member in members:
            if member.get("photo_url"):
                local_path = download_photo(member["photo_url"], member["name"])
                member["local_photo_url"] = local_path

    # 지역구 추출
    districts = list(set(m["district"] for m in members if m.get("district")))
    districts.sort()

    # 위원회 추출
    committees = list(set(m["committee"] for m in members if m.get("committee")))
    committees.sort()

    # JSON 저장
    data = {
        "members": members,
        "districts": [{"name": d, "region": extract_region(d)} for d in districts],
        "committees": [{"name": c} for c in committees],
    }

    output_file = OUTPUT_DIR / "members.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n[DONE] 저장 완료: {output_file}")
    print(f"       의원: {len(members)}명")
    print(f"       지역구: {len(districts)}개")
    print(f"       위원회: {len(committees)}개")


def extract_region(district: str) -> str:
    """지역구에서 권역 추출"""
    if not district:
        return ""

    # 시/구 이름 추출
    patterns = [
        r"(수원시)", r"(성남시)", r"(용인시)", r"(고양시)", r"(안양시)",
        r"(부천시)", r"(안산시)", r"(남양주시)", r"(화성시)", r"(평택시)",
        r"(의정부시)", r"(시흥시)", r"(파주시)", r"(광명시)", r"(김포시)",
        r"(군포시)", r"(광주시)", r"(이천시)", r"(양주시)", r"(오산시)",
        r"(구리시)", r"(안성시)", r"(포천시)", r"(의왕시)", r"(하남시)",
        r"(여주시)", r"(동두천시)", r"(과천시)", r"(양평군)", r"(가평군)",
        r"(연천군)",
    ]

    for pattern in patterns:
        match = re.search(pattern, district)
        if match:
            city = match.group(1)
            return city.replace("시", "권").replace("군", "권")

    return "기타"


if __name__ == "__main__":
    print("=" * 50)
    print("경기도의회 의원 데이터 스크래핑")
    print("=" * 50)

    members = scrape_all_members()

    if members:
        save_members_json(members, download_photos=True)
    else:
        print("[WARN] 의원 데이터를 찾지 못했습니다.")
        print("       웹페이지 구조가 변경되었을 수 있습니다.")

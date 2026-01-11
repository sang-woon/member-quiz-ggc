"""의원 사진 다운로드 스크립트"""
import json
import re
import time
from pathlib import Path
from urllib.parse import unquote
import requests

# 경로 설정
DATA_DIR = Path(__file__).parent
PHOTOS_DIR = Path(__file__).parent.parent.parent / "frontend" / "public" / "images" / "members"


def download_photos():
    """의원 사진 다운로드"""
    print("=" * 50)
    print("의원 사진 다운로드")
    print("=" * 50)

    # JSON 데이터 로드
    json_path = DATA_DIR / "members_updated.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    members = data["members"]
    print(f"[INFO] {len(members)}명 사진 다운로드 시작...")

    # 폴더 생성
    PHOTOS_DIR.mkdir(parents=True, exist_ok=True)

    downloaded = 0
    failed = 0
    skipped = 0

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        "Referer": "https://www.ggc.go.kr/",
    }

    for i, member in enumerate(members, 1):
        name = member["name"]
        photo_url = member["photo_url"]

        # 파일명 생성 (특수문자 제거)
        safe_name = re.sub(r"[^\w가-힣]", "", name)
        filename = f"{safe_name}.jpg"
        filepath = PHOTOS_DIR / filename

        # 이미 존재하면 스킵
        if filepath.exists():
            member["local_photo_url"] = f"/images/members/{filename}"
            skipped += 1
            print(f"[{i}/{len(members)}] {name} - SKIP (exists)")
            continue

        try:
            # URL 디코딩 (%5E -> ^)
            actual_url = unquote(photo_url)

            response = requests.get(actual_url, headers=headers, timeout=15)
            response.raise_for_status()

            with open(filepath, "wb") as f:
                f.write(response.content)

            member["local_photo_url"] = f"/images/members/{filename}"
            downloaded += 1
            print(f"[{i}/{len(members)}] {name} - OK")

        except Exception as e:
            member["local_photo_url"] = ""
            failed += 1
            print(f"[{i}/{len(members)}] {name} - FAILED: {e}")

        # 서버 부하 방지
        time.sleep(0.3)

    # 업데이트된 JSON 저장
    output_path = DATA_DIR / "members.json"

    # 지역구와 위원회 추출
    districts = list(set(m["district"] for m in members if m.get("district")))
    districts.sort()

    committees = set()
    for m in members:
        for c in m.get("committees", []):
            # 위원회명 정리 (위원장, 간사, 부위원장, 위원 등 제거)
            clean = re.sub(r"(위원장|부위원장|간사|위원)$", "", c)
            if clean:
                committees.add(clean)
    committees = sorted(list(committees))

    # 권역 매핑
    def get_region(district):
        if not district:
            return "기타"
        if "비례대표" in district:
            return "비례대표"
        patterns = [
            (r"수원시", "수원권"), (r"성남시", "성남권"), (r"용인시", "용인권"),
            (r"고양시", "고양권"), (r"안양시", "안양권"), (r"부천시", "부천권"),
            (r"안산시", "안산권"), (r"남양주시", "남양주권"), (r"화성시", "화성권"),
            (r"평택시", "평택권"), (r"의정부시", "의정부권"), (r"시흥시", "시흥권"),
            (r"파주시", "파주권"), (r"광명시", "광명권"), (r"김포시", "김포권"),
            (r"군포시", "군포권"), (r"광주시", "광주권"), (r"이천시", "이천권"),
            (r"양주시", "양주권"), (r"오산시", "오산권"), (r"구리시", "구리권"),
            (r"안성시", "안성권"), (r"포천시", "포천권"), (r"의왕시", "의왕권"),
            (r"하남시", "하남권"), (r"여주시", "여주권"), (r"동두천시", "동두천권"),
            (r"과천시", "과천권"), (r"양평군", "양평권"), (r"가평군", "가평권"),
            (r"연천군", "연천권"),
        ]
        for pattern, region in patterns:
            if re.search(pattern, district):
                return region
        return "기타"

    final_data = {
        "members": members,
        "districts": [{"name": d, "region": get_region(d)} for d in districts],
        "committees": [{"name": c} for c in committees],
        "total": len(members),
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 50)
    print(f"[DONE] 다운로드 완료!")
    print(f"       성공: {downloaded}개")
    print(f"       스킵: {skipped}개")
    print(f"       실패: {failed}개")
    print(f"       저장: {output_path}")
    print("=" * 50)


if __name__ == "__main__":
    download_photos()

"""실제 스크래핑 데이터로 DB 시드"""
import json
import re
import sys
from pathlib import Path

# 프로젝트 루트를 path에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database.database import engine, SessionLocal, Base
from app.models import District, Committee, Member, MemberCommittee


def load_member_data():
    """members.json에서 데이터 로드"""
    data_path = Path(__file__).parent / "members.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def seed_districts(db, districts_data):
    """지역구 시드 데이터"""
    for d in districts_data:
        district = District(name=d["name"], region=d["region"])
        db.add(district)
    db.commit()
    print(f"[OK] {len(districts_data)}개 지역구 추가됨")


def seed_committees(db, committees_data):
    """위원회 시드 데이터"""
    for c in committees_data:
        committee = Committee(name=c["name"])
        db.add(committee)
    db.commit()
    print(f"[OK] {len(committees_data)}개 위원회 추가됨")


def seed_members(db, members_data, districts_data):
    """의원 시드 데이터"""
    # 지역구 이름 -> ID 매핑
    district_map = {}
    for district in db.query(District).all():
        district_map[district.name] = district.id

    added = 0
    for m in members_data:
        district_id = district_map.get(m.get("district"))
        if not district_id:
            # 지역구가 없으면 None으로 설정
            district_id = None

        photo_url = m.get("local_photo_url", "") or ""

        member = Member(
            name=m["name"],
            photo_url=photo_url,
            party=m.get("party", ""),
            district_id=district_id,
            term=11,
        )
        db.add(member)
        added += 1

    db.commit()
    print(f"[OK] {added}명 의원 추가됨")


def seed_member_committees(db, members_data, committees_data):
    """의원-위원회 연결 시드 데이터"""
    # 위원회 이름 -> ID 매핑
    committee_map = {}
    for committee in db.query(Committee).all():
        committee_map[committee.name] = committee.id

    # 의원 이름 -> ID 매핑
    member_map = {}
    for member in db.query(Member).all():
        member_map[member.name] = member.id

    added = 0
    for m in members_data:
        member_id = member_map.get(m["name"])
        if not member_id:
            continue

        for c in m.get("committees", []):
            # 위원회명에서 역할 추출 (위원장, 부위원장, 간사, 위원)
            is_chairman = "위원장" in c and "부위원장" not in c

            # 위원회명 정리
            clean_name = re.sub(r"(위원장|부위원장|간사|위원)$", "", c)
            committee_id = committee_map.get(clean_name)

            if committee_id:
                mc = MemberCommittee(
                    member_id=member_id,
                    committee_id=committee_id,
                    is_chairman=is_chairman,
                )
                db.add(mc)
                added += 1

    db.commit()
    print(f"[OK] {added}개 의원-위원회 연결 추가됨")


def run_seed():
    """시드 데이터 실행"""
    print("=" * 50)
    print("[SEED] 시드 데이터 생성 시작...")
    print("=" * 50)

    # 데이터 로드
    data = load_member_data()
    members_data = data["members"]
    districts_data = data["districts"]
    committees_data = data["committees"]

    print(f"[INFO] 로드된 데이터:")
    print(f"   - 의원: {len(members_data)}명")
    print(f"   - 지역구: {len(districts_data)}개")
    print(f"   - 위원회: {len(committees_data)}개")

    # 테이블 생성
    Base.metadata.create_all(bind=engine)
    print("[OK] 테이블 생성됨")

    db = SessionLocal()
    try:
        # 기존 데이터 삭제 (항상 새로 시드)
        existing = db.query(Member).count()
        if existing > 0:
            print(f"[INFO] 기존 데이터 삭제 중... ({existing}명)")
            db.query(MemberCommittee).delete()
            db.query(Member).delete()
            db.query(Committee).delete()
            db.query(District).delete()
            db.commit()
            print("[OK] 기존 데이터 삭제됨")

        seed_districts(db, districts_data)
        seed_committees(db, committees_data)
        seed_members(db, members_data, districts_data)
        seed_member_committees(db, members_data, committees_data)

        print("\n" + "=" * 50)
        print("[DONE] 시드 데이터 생성 완료!")
        print("=" * 50)

        # 확인
        member_count = db.query(Member).count()
        district_count = db.query(District).count()
        committee_count = db.query(Committee).count()
        mc_count = db.query(MemberCommittee).count()

        print(f"\n[INFO] 데이터 현황:")
        print(f"   - 의원: {member_count}명")
        print(f"   - 지역구: {district_count}개")
        print(f"   - 위원회: {committee_count}개")
        print(f"   - 의원-위원회 연결: {mc_count}개")

    finally:
        db.close()


if __name__ == "__main__":
    run_seed()

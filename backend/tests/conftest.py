"""pytest 설정 및 fixture"""
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.database import Base, get_db
from app.models import District, Committee, Member, MemberCommittee


# 테스트용 인메모리 SQLite DB
TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """테스트용 DB 세션 fixture"""
    Base.metadata.create_all(bind=engine)
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def seeded_db(db_session):
    """시드 데이터가 포함된 DB 세션 fixture"""
    # 지역구 추가
    districts = [
        District(id=1, name="수원시갑", region="수원권"),
        District(id=2, name="성남시분당갑", region="성남권"),
        District(id=3, name="비례대표", region="비례대표"),
    ]
    for d in districts:
        db_session.add(d)
    db_session.commit()

    # 위원회 추가
    committees = [
        Committee(id=1, name="운영위원회"),
        Committee(id=2, name="기획재정위원회"),
        Committee(id=3, name="행정안전위원회"),
    ]
    for c in committees:
        db_session.add(c)
    db_session.commit()

    # 의원 추가
    members = [
        Member(id=1, name="김철수", photo_url="/images/members/김철수.jpg", party="더불어민주당", district_id=1, term=11),
        Member(id=2, name="이영희", photo_url="/images/members/이영희.jpg", party="국민의힘", district_id=2, term=11),
        Member(id=3, name="박지성", photo_url="/images/members/박지성.jpg", party="더불어민주당", district_id=1, term=11),
        Member(id=4, name="최유리", photo_url="/images/members/최유리.jpg", party="국민의힘", district_id=3, term=11),
        Member(id=5, name="정민수", photo_url="/images/members/정민수.jpg", party="더불어민주당", district_id=2, term=11),
    ]
    for m in members:
        db_session.add(m)
    db_session.commit()

    # 의원-위원회 연결
    member_committees = [
        MemberCommittee(member_id=1, committee_id=1, is_chairman=True),
        MemberCommittee(member_id=1, committee_id=2, is_chairman=False),
        MemberCommittee(member_id=2, committee_id=2, is_chairman=False),
        MemberCommittee(member_id=3, committee_id=3, is_chairman=False),
        MemberCommittee(member_id=4, committee_id=1, is_chairman=False),
        MemberCommittee(member_id=5, committee_id=3, is_chairman=True),
    ]
    for mc in member_committees:
        db_session.add(mc)
    db_session.commit()

    yield db_session


def override_get_db(db_session):
    """DB 의존성 오버라이드 함수"""
    def _override():
        try:
            yield db_session
        finally:
            pass
    return _override


@pytest_asyncio.fixture
async def client(seeded_db):
    """비동기 HTTP 클라이언트 fixture"""
    app.dependency_overrides[get_db] = override_get_db(seeded_db)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

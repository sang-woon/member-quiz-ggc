"""의원 API 테스트 (RED 상태 - 아직 구현 없음)"""
import pytest


class TestGetMembersList:
    """의원 목록 조회 테스트"""

    @pytest.mark.asyncio
    async def test_get_members_list(self, client):
        """의원 목록 조회 시 200 응답과 목록 반환"""
        response = await client.get("/api/members")

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) > 0

    @pytest.mark.asyncio
    async def test_members_list_has_required_fields(self, client):
        """의원 목록의 각 항목에 필수 필드 존재"""
        response = await client.get("/api/members")
        data = response.json()
        member = data["data"][0]

        assert "id" in member
        assert "name" in member
        assert "photoUrl" in member
        assert "party" in member
        assert "districtId" in member
        assert "districtName" in member

    @pytest.mark.asyncio
    async def test_get_members_with_pagination(self, client):
        """의원 목록 페이지네이션 테스트"""
        response = await client.get("/api/members?page=1&size=2")

        assert response.status_code == 200
        data = response.json()
        assert "meta" in data
        assert data["meta"]["page"] == 1
        assert data["meta"]["size"] == 2
        assert len(data["data"]) <= 2


class TestGetMembersFilter:
    """의원 목록 필터링 테스트"""

    @pytest.mark.asyncio
    async def test_filter_by_district(self, client):
        """지역구별 의원 필터링"""
        response = await client.get("/api/members?districtId=1")

        assert response.status_code == 200
        data = response.json()
        # 모든 의원이 해당 지역구 소속인지 확인
        for member in data["data"]:
            assert member["districtId"] == 1

    @pytest.mark.asyncio
    async def test_filter_by_committee(self, client):
        """위원회별 의원 필터링"""
        response = await client.get("/api/members?committeeId=1")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["data"], list)

    @pytest.mark.asyncio
    async def test_filter_by_party(self, client):
        """정당별 의원 필터링"""
        response = await client.get("/api/members?party=더불어민주당")

        assert response.status_code == 200
        data = response.json()
        for member in data["data"]:
            assert member["party"] == "더불어민주당"


class TestGetMemberDetail:
    """의원 상세 조회 테스트"""

    @pytest.mark.asyncio
    async def test_get_member_detail(self, client):
        """의원 상세 조회 시 200 응답"""
        response = await client.get("/api/members/1")

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert data["data"]["id"] == 1

    @pytest.mark.asyncio
    async def test_member_detail_has_committees(self, client):
        """의원 상세 조회 시 위원회 목록 포함"""
        response = await client.get("/api/members/1")

        assert response.status_code == 200
        data = response.json()
        assert "committees" in data["data"]
        assert isinstance(data["data"]["committees"], list)

    @pytest.mark.asyncio
    async def test_get_member_not_found(self, client):
        """존재하지 않는 의원 조회 시 404 응답"""
        response = await client.get("/api/members/9999")

        assert response.status_code == 404

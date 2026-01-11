"""필터 API 테스트 (RED 상태 - 아직 구현 없음)"""
import pytest


class TestGetDistricts:
    """지역구 목록 조회 테스트"""

    @pytest.mark.asyncio
    async def test_get_districts(self, client):
        """지역구 목록 조회 시 200 응답"""
        response = await client.get("/api/districts")

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)

    @pytest.mark.asyncio
    async def test_districts_have_required_fields(self, client):
        """지역구 목록의 각 항목에 필수 필드 존재"""
        response = await client.get("/api/districts")
        data = response.json()
        district = data["data"][0]

        assert "id" in district
        assert "name" in district
        assert "region" in district

    @pytest.mark.asyncio
    async def test_districts_count(self, client):
        """지역구 목록 개수 확인"""
        response = await client.get("/api/districts")
        data = response.json()

        # 테스트 데이터에는 3개의 지역구가 있음
        assert len(data["data"]) == 3


class TestGetCommittees:
    """위원회 목록 조회 테스트"""

    @pytest.mark.asyncio
    async def test_get_committees(self, client):
        """위원회 목록 조회 시 200 응답"""
        response = await client.get("/api/committees")

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)

    @pytest.mark.asyncio
    async def test_committees_have_required_fields(self, client):
        """위원회 목록의 각 항목에 필수 필드 존재"""
        response = await client.get("/api/committees")
        data = response.json()
        committee = data["data"][0]

        assert "id" in committee
        assert "name" in committee

    @pytest.mark.asyncio
    async def test_committees_count(self, client):
        """위원회 목록 개수 확인"""
        response = await client.get("/api/committees")
        data = response.json()

        # 테스트 데이터에는 3개의 위원회가 있음
        assert len(data["data"]) == 3

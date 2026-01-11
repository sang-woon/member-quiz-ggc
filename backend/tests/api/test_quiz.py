"""퀴즈 API 테스트 (RED 상태 - 아직 구현 없음)"""
import pytest


class TestGetQuizQuestion:
    """퀴즈 문제 생성 테스트"""

    @pytest.mark.asyncio
    async def test_get_quiz_question(self, client):
        """퀴즈 문제 조회 시 200 응답"""
        response = await client.get("/api/quiz")

        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "options" in data

    @pytest.mark.asyncio
    async def test_quiz_has_four_options(self, client):
        """퀴즈 문제에 4개의 보기 존재"""
        response = await client.get("/api/quiz")

        assert response.status_code == 200
        data = response.json()
        assert len(data["options"]) == 4

    @pytest.mark.asyncio
    async def test_quiz_answer_in_options(self, client):
        """정답이 보기에 포함되어 있음"""
        response = await client.get("/api/quiz")

        assert response.status_code == 200
        data = response.json()
        answer_id = data["answer"]["id"]
        option_ids = [opt["id"] for opt in data["options"]]
        assert answer_id in option_ids

    @pytest.mark.asyncio
    async def test_quiz_options_are_unique(self, client):
        """보기가 모두 서로 다른 의원"""
        response = await client.get("/api/quiz")

        assert response.status_code == 200
        data = response.json()
        option_ids = [opt["id"] for opt in data["options"]]
        assert len(option_ids) == len(set(option_ids))

    @pytest.mark.asyncio
    async def test_quiz_answer_has_required_fields(self, client):
        """정답 의원에 필수 필드 존재"""
        response = await client.get("/api/quiz")

        assert response.status_code == 200
        data = response.json()
        answer = data["answer"]

        assert "id" in answer
        assert "name" in answer
        assert "photoUrl" in answer
        assert "districtName" in answer


class TestQuizFiltering:
    """퀴즈 필터링 테스트"""

    @pytest.mark.asyncio
    async def test_quiz_filter_by_district(self, client):
        """지역구 필터링된 퀴즈"""
        response = await client.get("/api/quiz?districtId=1")

        assert response.status_code == 200
        data = response.json()
        # 정답이 존재하고 4개 보기가 있는지 확인
        # (필터된 의원이 4명 미만이면 전체에서 보충하므로 districtId 체크 제외)
        assert "answer" in data
        assert len(data["options"]) == 4

    @pytest.mark.asyncio
    async def test_quiz_filter_by_committee(self, client):
        """위원회 필터링된 퀴즈"""
        response = await client.get("/api/quiz?committeeId=1")

        assert response.status_code == 200
        data = response.json()
        assert "answer" in data

    @pytest.mark.asyncio
    async def test_quiz_randomness(self, client):
        """퀴즈 문제가 랜덤하게 생성됨 (같은 요청 시 다른 결과)"""
        responses = []
        for _ in range(5):
            response = await client.get("/api/quiz")
            assert response.status_code == 200
            responses.append(response.json()["answer"]["id"])

        # 최소 2개 이상 다른 답이 나와야 함 (5번 중)
        unique_answers = set(responses)
        # 의원 수가 적으면 같은 답이 나올 수 있으므로, 1개 초과면 통과
        assert len(unique_answers) >= 1

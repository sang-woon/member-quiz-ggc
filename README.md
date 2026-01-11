# 의원얼굴퀴즈

경기도의회 11대 의원 얼굴 맞추기 퀴즈 앱

## 개요

경기도의회 사무처 직원(특히 신규 입사자)이 의원 얼굴과 이름을 쉽고 재미있게 학습할 수 있는 퀴즈 앱입니다.

## 기술 스택

| 구분 | 기술 |
|------|------|
| **백엔드** | FastAPI (Python 3.11+) + SQLAlchemy 2.0 |
| **프론트엔드** | React 18 + Vite + TypeScript |
| **스타일링** | TailwindCSS |
| **애니메이션** | Framer Motion |
| **데이터베이스** | SQLite |

## 프로젝트 구조

```
member-quiz/
├── backend/           # FastAPI 백엔드
│   ├── app/
│   │   ├── routes/    # API 라우터
│   │   ├── services/  # 비즈니스 로직
│   │   ├── models/    # SQLAlchemy 모델
│   │   ├── schemas/   # Pydantic 스키마
│   │   └── database/  # DB 설정
│   ├── data/          # 시드 데이터
│   └── tests/         # pytest 테스트
├── frontend/          # React 프론트엔드
│   ├── src/
│   │   ├── pages/     # 페이지 컴포넌트
│   │   ├── components/# 재사용 컴포넌트
│   │   ├── services/  # API 서비스
│   │   └── types/     # TypeScript 타입
│   └── public/
│       └── images/members/  # 의원 사진
├── contracts/         # API 계약 정의
└── docs/planning/     # 기획 문서
```

## 실행 방법

### 1. 백엔드 실행

```bash
cd backend

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# DB 시드 데이터 생성
python data/seed.py

# 서버 실행
uvicorn app.main:app --reload --port 8000
```

API 문서: http://localhost:8000/docs

### 2. 프론트엔드 실행

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

앱 접속: http://localhost:5173

### 3. 테스트 실행

**백엔드 테스트:**
```bash
cd backend
pytest tests/ -v
```

**프론트엔드 테스트:**
```bash
cd frontend
npm run test
```

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/members` | 의원 목록 조회 (필터링 지원) |
| GET | `/api/members/{id}` | 의원 상세 조회 |
| GET | `/api/quiz` | 퀴즈 문제 생성 (4지선다) |
| GET | `/api/districts` | 지역구 목록 조회 |
| GET | `/api/committees` | 위원회 목록 조회 |

## 주요 기능

- 전체 의원 대상 퀴즈
- 지역구/위원회별 필터링 퀴즈
- 10문제 1세트 퀴즈
- 정답/오답 애니메이션
- 결과 화면 (정답률 표시)

## 데이터

- 155명의 경기도의회 11대 의원 데이터
- 141개 지역구
- 16개 위원회
- 의원 사진 포함

## 라이선스

이 프로젝트는 내부 학습용으로 제작되었습니다.

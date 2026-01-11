# Coding Convention & AI Collaboration Guide

> 의원얼굴퀴즈 - 고품질/유지보수/보안을 위한 인간-AI 협업 운영 지침서

---

## MVP 캡슐

| # | 항목 | 내용 |
|---|------|------|
| 1 | 목표 | 경기도의회 직원이 의원 얼굴과 이름을 쉽고 재미있게 학습 |
| 2 | 페르소나 | 경기도의회 사무처 직원 (특히 신규 입사자) |
| 3 | 핵심 기능 | FEAT-1: 얼굴 보고 이름 맞추기 퀴즈 |
| 4 | 성공 지표 (노스스타) | 사용자가 전체 의원 정답률 80% 이상 달성 |
| 5 | 입력 지표 | 퀴즈 완료 횟수, 일일 활성 사용자 |
| 6 | 비기능 요구 | 모바일/PC 반응형 지원 |
| 7 | Out-of-scope | 로그인/회원가입, 학습 진도 저장, 랭킹 시스템 |
| 8 | Top 리스크 | 의원 사진 데이터 확보 및 최신 유지 |
| 9 | 완화/실험 | 경기도의회 공식 홈페이지 데이터 활용 |
| 10 | 다음 단계 | 의원 데이터 수집 및 정리 |

---

## 1. 핵심 원칙

### 1.1 신뢰하되, 검증하라 (Don't Trust, Verify)

AI가 생성한 코드는 반드시 검증해야 합니다:

- [ ] 코드 리뷰: 생성된 코드 직접 확인
- [ ] 테스트 실행: 자동화 테스트 통과 확인
- [ ] 동작 확인: 실제로 실행하여 기대 동작 확인

### 1.2 최종 책임은 인간에게

- AI는 도구이고, 최종 결정과 책임은 개발자에게 있습니다
- 이해하지 못하는 코드는 사용하지 않습니다
- 의심스러운 부분은 반드시 질문합니다

---

## 2. 프로젝트 구조

### 2.1 디렉토리 구조

```
member-quiz/
├── frontend/                    # React + Vite 프론트엔드
│   ├── src/
│   │   ├── components/         # 재사용 컴포넌트
│   │   │   ├── common/         # 버튼, 카드 등 공통
│   │   │   └── quiz/           # 퀴즈 관련 컴포넌트
│   │   ├── pages/              # 페이지 컴포넌트
│   │   ├── hooks/              # 커스텀 훅
│   │   ├── services/           # API 호출
│   │   ├── types/              # TypeScript 타입
│   │   ├── utils/              # 유틸리티 함수
│   │   ├── mocks/              # MSW 목 핸들러
│   │   └── __tests__/          # 테스트 파일
│   ├── public/
│   │   └── images/
│   │       └── members/        # 의원 사진
│   └── e2e/                    # E2E 테스트
│
├── backend/                     # FastAPI 백엔드
│   ├── app/
│   │   ├── models/             # SQLAlchemy 모델
│   │   ├── routes/             # API 라우트
│   │   ├── schemas/            # Pydantic 스키마
│   │   ├── services/           # 비즈니스 로직
│   │   └── database/           # DB 설정, SQLite 파일
│   ├── tests/                  # pytest 테스트
│   └── data/                   # 시드 데이터
│
├── contracts/                   # API 계약 (BE/FE 공유)
│   └── api.contract.ts
│
├── docs/
│   └── planning/               # 기획 문서 (이 문서들)
│
└── docker-compose.yml          # 로컬 개발 환경 (선택)
```

### 2.2 네이밍 규칙

| 대상 | 규칙 | 예시 |
|------|------|------|
| 파일 (React 컴포넌트) | PascalCase | `QuizCard.tsx` |
| 파일 (훅) | camelCase + use | `useQuiz.ts` |
| 파일 (유틸) | camelCase | `formatMemberName.ts` |
| 파일 (Python) | snake_case | `member_service.py` |
| React 컴포넌트 | PascalCase | `QuizCard` |
| 함수/변수 (JS/TS) | camelCase | `getMemberById` |
| 함수/변수 (Python) | snake_case | `get_member_by_id` |
| 상수 | UPPER_SNAKE | `MAX_QUIZ_COUNT` |
| CSS 클래스 (Tailwind) | kebab-case | `quiz-card` |
| API 엔드포인트 | kebab-case | `/api/members` |

---

## 3. 아키텍처 원칙

### 3.1 뼈대 먼저 (Skeleton First)

1. 전체 구조를 먼저 잡고
2. 빈 함수/컴포넌트로 스켈레톤 생성
3. 하나씩 구현 채워나가기

### 3.2 작은 모듈로 분해

- 한 파일에 150줄 이하 권장
- 한 함수에 30줄 이하 권장
- 한 컴포넌트에 100줄 이하 권장

### 3.3 관심사 분리

| 레이어 | 역할 | 예시 |
|--------|------|------|
| UI | 화면 표시 | React 컴포넌트 |
| 상태 | 로컬 상태 관리 | useState, useReducer |
| 서비스 | API 통신 | fetch 래퍼 |
| 유틸 | 순수 함수 | 데이터 변환, 셔플 |

---

## 4. AI 소통 원칙

### 4.1 하나의 채팅 = 하나의 작업

- 한 번에 하나의 명확한 작업만 요청
- 작업 완료 후 다음 작업 진행
- 컨텍스트가 길어지면 새 대화 시작

### 4.2 컨텍스트 명시

**좋은 예:**
> "TASKS 문서의 T2.1을 구현해주세요.
> Database Design의 MEMBER 테이블을 참조하고,
> TRD의 FastAPI 스택을 따라주세요."

**나쁜 예:**
> "API 만들어줘"

### 4.3 프롬프트 템플릿

```
## 작업
{{무엇을 해야 하는지}}

## 참조 문서
- {{문서명}} 섹션 {{번호}}

## 제약 조건
- {{지켜야 할 것}}

## 예상 결과
- {{생성될 파일}}
- {{기대 동작}}
```

---

## 5. 코딩 스타일

### 5.1 TypeScript (프론트엔드)

```typescript
// 타입 정의
interface Member {
  id: number;
  name: string;
  photoUrl: string;
  party: string | null;
  districtId: number;
}

// 컴포넌트
interface QuizCardProps {
  member: Member;
  options: Member[];
  onAnswer: (selectedId: number) => void;
}

export function QuizCard({ member, options, onAnswer }: QuizCardProps) {
  return (
    <div className="quiz-card">
      {/* ... */}
    </div>
  );
}

// 훅
export function useQuiz(filter?: QuizFilter) {
  const [currentQuestion, setCurrentQuestion] = useState<QuizQuestion | null>(null);
  const [score, setScore] = useState(0);

  // ...

  return { currentQuestion, score, submitAnswer };
}
```

### 5.2 Python (백엔드)

```python
# 모델
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    photo_url = Column(String(500), nullable=False)
    party = Column(String(50), nullable=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False)

    district = relationship("District", back_populates="members")


# 스키마
from pydantic import BaseModel

class MemberBase(BaseModel):
    name: str
    photo_url: str
    party: str | None = None
    district_id: int

class MemberResponse(MemberBase):
    id: int

    class Config:
        from_attributes = True


# 라우트
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/members", tags=["members"])

@router.get("/", response_model=list[MemberResponse])
async def get_members(
    district_id: int | None = None,
    db: Session = Depends(get_db)
):
    """의원 목록 조회"""
    return member_service.get_members(db, district_id=district_id)
```

---

## 6. 보안 체크리스트

### 6.1 절대 금지

- [ ] 비밀정보 하드코딩 금지 (API 키, 비밀번호)
- [ ] .env 파일 커밋 금지
- [ ] SQL 직접 문자열 조합 금지 (ORM 사용)

### 6.2 필수 적용

- [ ] 모든 사용자 입력 검증 (서버 측 - Pydantic)
- [ ] CORS 설정 (프론트엔드 도메인만 허용)
- [ ] 배포 시 HTTPS 필수

### 6.3 환경 변수 관리

```bash
# .env.example (커밋 O)
DATABASE_URL=sqlite:///./members.db
CORS_ORIGINS=http://localhost:5173

# .env (커밋 X)
DATABASE_URL=sqlite:///./members.db
CORS_ORIGINS=https://quiz.example.com
```

**.gitignore:**
```
.env
*.db
__pycache__/
node_modules/
dist/
```

---

## 7. 테스트 워크플로우

### 7.1 테스트 구조

```
frontend/
├── src/__tests__/
│   ├── components/
│   │   └── QuizCard.test.tsx
│   └── hooks/
│       └── useQuiz.test.ts
└── e2e/
    └── quiz.spec.ts

backend/
└── tests/
    ├── api/
    │   └── test_members.py
    └── services/
        └── test_quiz_service.py
```

### 7.2 테스트 실행

```bash
# 백엔드
cd backend
pytest -v --cov=app

# 프론트엔드
cd frontend
npm run test

# E2E
npx playwright test
```

### 7.3 오류 로그 공유 규칙

오류 발생 시 AI에게 전달할 정보:

1. 전체 에러 메시지
2. 관련 코드 스니펫
3. 재현 단계
4. 이미 시도한 해결책

---

## 8. Git 워크플로우

### 8.1 브랜치 전략

```
main          # 프로덕션 (배포 가능 상태)
├── develop   # 개발 통합
│   ├── feature/quiz-ui
│   ├── feature/api-members
│   └── fix/image-loading
```

### 8.2 커밋 메시지

```
<type>(<scope>): <subject>

<body>
```

**타입:**
- `feat`: 새 기능
- `fix`: 버그 수정
- `refactor`: 리팩토링
- `docs`: 문서
- `test`: 테스트
- `chore`: 기타

**예시:**
```
feat(quiz): 퀴즈 보기 버튼 4지선다 구현

- 4개 보기 칼라풀하게 표시
- 정답/오답 애니메이션 추가
- Design System 05 적용
```

### 8.3 PR 규칙

- [ ] 테스트 통과
- [ ] 린트 통과
- [ ] 코드 리뷰 (self-review)

---

## 9. 코드 품질 도구

### 9.1 프론트엔드

```json
// package.json scripts
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx",
    "format": "prettier --write .",
    "test": "vitest",
    "type-check": "tsc --noEmit"
  }
}
```

**ESLint 설정 (.eslintrc.cjs):**
```javascript
module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh'],
  rules: {
    'react-refresh/only-export-components': 'warn',
  },
}
```

### 9.2 백엔드

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
select = ["E", "F", "I", "UP"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
```

**실행:**
```bash
# 린트
ruff check app/ tests/

# 포맷
ruff format app/ tests/

# 타입 체크 (선택)
mypy app/
```

---

## 10. 로컬 개발 환경

### 10.1 필수 도구

| 도구 | 버전 | 용도 |
|------|------|------|
| Node.js | 18+ | 프론트엔드 |
| Python | 3.11+ | 백엔드 |
| Git | 최신 | 버전 관리 |

### 10.2 초기 설정

```bash
# 프론트엔드
cd frontend
npm install
npm run dev  # http://localhost:5173

# 백엔드
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload  # http://localhost:8000
```

### 10.3 동시 실행 (선택)

```bash
# 터미널 1: 백엔드
cd backend && uvicorn app.main:app --reload

# 터미널 2: 프론트엔드
cd frontend && npm run dev
```

---

## Decision Log 참조

| 결정 | 이유 |
|------|------|
| Ruff 사용 | Black + isort + flake8 통합, 빠름 |
| ESLint + Prettier | 프론트엔드 표준 도구 |
| 150줄 제한 | 작은 파일 = 읽기 쉬움 = 유지보수 용이 |
| CORS 설정 필수 | 프론트엔드-백엔드 분리 아키텍처 |

# Design System (기초 디자인 시스템)

> 의원얼굴퀴즈의 디자인 언어 - 듀오링고 스타일 + 공식적 톤

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

## 1. 디자인 철학

### 1.1 핵심 가치

| 가치 | 설명 | 구현 방법 |
|------|------|----------|
| 재미 (Fun) | 게임처럼 즐거운 학습 경험 | 칼라풀한 색상, 애니메이션, 피드백 효과 |
| 명료함 (Clarity) | 한눈에 이해되는 UI | 충분한 여백, 명확한 버튼, 큰 사진 |
| 신뢰감 (Trust) | 공공기관다운 격식 | 정제된 톤, 공식적 문구 |

### 1.2 참고 서비스 (무드보드)

| 서비스 | 참고할 점 | 참고하지 않을 점 |
|--------|----------|-----------------|
| 듀오링고 | 칼라풀한 색상, 재미있는 피드백, 진행 표시 | 캐릭터/마스코트 (공공앱에 부적합) |
| 카훗 (Kahoot) | 큰 버튼, 명확한 정답/오답 표시 | 과한 사운드 효과 |
| 경기도의회 홈페이지 | 신뢰감 있는 톤, 공식 로고 색상 참고 | 딱딱한 레이아웃 |

---

## 2. 컬러 팔레트

### 2.1 역할 기반 컬러

| 역할 | 컬러명 | Hex | 사용처 |
|------|------|-----|--------|
| **Primary** | 경기 블루 | `#1E40AF` | 주요 버튼, 헤더, 강조 |
| **Primary Light** | 라이트 블루 | `#DBEAFE` | 호버 배경, 선택 표시 |
| **Secondary** | 웜 그린 | `#059669` | 정답 표시, 진행률 |
| **Surface** | 화이트 | `#FFFFFF` | 카드, 버튼 배경 |
| **Background** | 라이트 그레이 | `#F3F4F6` | 전체 배경 |
| **Text Primary** | 다크 그레이 | `#1F2937` | 주요 텍스트 |
| **Text Secondary** | 미디엄 그레이 | `#6B7280` | 보조 텍스트 |

### 2.2 피드백 컬러

| 상태 | 컬러 | Hex | 사용처 |
|------|------|-----|--------|
| **Success** | 그린 | `#22C55E` | 정답 피드백, 완료 표시 |
| **Error** | 레드 | `#EF4444` | 오답 피드백 |
| **Warning** | 옐로우 | `#EAB308` | 주의 메시지 |
| **Info** | 블루 | `#3B82F6` | 정보, 힌트 |

### 2.3 퀴즈 보기 컬러 (듀오링고 스타일)

| 보기 | 기본 배경 | 호버 | 선택 시 |
|------|----------|------|---------|
| 1번 | `#FEF3C7` (연노랑) | `#FDE68A` | 테두리 강조 |
| 2번 | `#DBEAFE` (연파랑) | `#BFDBFE` | 테두리 강조 |
| 3번 | `#FCE7F3` (연핑크) | `#FBCFE8` | 테두리 강조 |
| 4번 | `#D1FAE5` (연초록) | `#A7F3D0` | 테두리 강조 |

### 2.4 다크 모드

- MVP에서는 **라이트 모드만 지원**
- 다크 모드는 v2에서 검토

---

## 3. 타이포그래피

### 3.1 폰트 패밀리

| 용도 | 폰트 | 대안 |
|------|------|------|
| 본문/UI | Pretendard | system-ui, -apple-system, sans-serif |
| 숫자/점수 | Pretendard | inherit |

**CDN 링크:**
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css" />
```

### 3.2 타입 스케일

| 이름 | 크기 | 굵기 | 용도 |
|------|------|------|------|
| Display | 48px | Bold (700) | 결과 점수 |
| H1 | 32px | Bold (700) | 페이지 제목 |
| H2 | 24px | SemiBold (600) | 섹션 제목 |
| H3 | 20px | SemiBold (600) | 퀴즈 질문 |
| Body Large | 18px | Medium (500) | 보기 텍스트 |
| Body | 16px | Regular (400) | 기본 본문 |
| Caption | 14px | Regular (400) | 부가 정보, 힌트 |
| Small | 12px | Regular (400) | 진행률, 문제 번호 |

---

## 4. 간격 토큰 (Spacing)

| 이름 | 값 | Tailwind | 용도 |
|------|-----|----------|------|
| xs | 4px | `p-1` | 아이콘-텍스트 간격 |
| sm | 8px | `p-2` | 요소 내부 여백 |
| md | 16px | `p-4` | 카드 내부 여백 |
| lg | 24px | `p-6` | 섹션 간 간격 |
| xl | 32px | `p-8` | 큰 섹션 구분 |
| 2xl | 48px | `p-12` | 페이지 여백 |

---

## 5. 기본 컴포넌트

### 5.1 버튼 (Button)

**크기:**
| 크기 | 높이 | 패딩 | 폰트 |
|------|------|------|------|
| Large | 56px | 24px | 18px Bold |
| Medium | 48px | 20px | 16px Medium |
| Small | 40px | 16px | 14px Medium |

**변형:**
| 변형 | 기본 | 호버 | 비활성 |
|------|------|------|--------|
| Primary | 블루 배경 + 흰 글씨 | 약간 어둡게 | 50% 투명도 |
| Secondary | 흰 배경 + 블루 테두리 | 블루 배경 | 50% 투명도 |
| Ghost | 투명 + 블루 글씨 | 연한 블루 배경 | 50% 투명도 |

**퀴즈 보기 버튼 (특수):**
```css
/* 기본 상태 */
.answer-option {
  min-height: 64px;
  border-radius: 16px;
  border: 3px solid transparent;
  font-size: 18px;
  font-weight: 500;
  transition: all 0.2s;
}

/* 호버 */
.answer-option:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* 정답 */
.answer-option.correct {
  background: #22C55E;
  color: white;
  border-color: #16A34A;
}

/* 오답 */
.answer-option.wrong {
  background: #EF4444;
  color: white;
  border-color: #DC2626;
}
```

### 5.2 카드 (Card)

```css
.card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.07);
  padding: 24px;
}

.card-elevated {
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}
```

### 5.3 의원 사진 컨테이너

```css
.member-photo {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #E5E7EB;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* 모바일 */
@media (max-width: 640px) {
  .member-photo {
    width: 160px;
    height: 160px;
  }
}
```

### 5.4 진행률 바 (Progress Bar)

```css
.progress-bar {
  height: 8px;
  background: #E5E7EB;
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #1E40AF, #3B82F6);
  transition: width 0.3s ease;
}
```

---

## 6. 애니메이션

### 6.1 기본 원칙

- **빠르게**: 200-300ms (답답하지 않게)
- **자연스럽게**: ease-out 커브
- **의미있게**: 피드백 전달 목적

### 6.2 주요 애니메이션

**정답 시:**
```css
@keyframes correct-bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.correct-animation {
  animation: correct-bounce 0.4s ease-out;
  background: #22C55E;
}
```

**오답 시:**
```css
@keyframes wrong-shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-8px); }
  75% { transform: translateX(8px); }
}

.wrong-animation {
  animation: wrong-shake 0.4s ease-out;
  background: #EF4444;
}
```

**카드 진입:**
```css
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in {
  animation: fade-in-up 0.3s ease-out;
}
```

### 6.3 Framer Motion 예시

```tsx
// 보기 버튼
<motion.button
  whileHover={{ scale: 1.02, y: -2 }}
  whileTap={{ scale: 0.98 }}
  transition={{ type: "spring", stiffness: 400 }}
>
  {option.name}
</motion.button>

// 정답 피드백
<motion.div
  initial={{ scale: 0.8, opacity: 0 }}
  animate={{ scale: 1, opacity: 1 }}
  transition={{ type: "spring", stiffness: 500 }}
>
  정답입니다!
</motion.div>
```

---

## 7. 접근성 체크리스트

### 7.1 필수 (MVP)

- [x] **색상 대비**: 텍스트와 배경 대비율 4.5:1 이상
- [x] **포커스 링**: 키보드 탐색 시 포커스 표시 명확
- [x] **클릭 영역**: 버튼 최소 48x48px (모바일 터치 고려)
- [x] **에러 표시**: 색상만으로 구분하지 않음 (아이콘 병행)
- [x] **폰트 크기**: 본문 최소 16px

### 7.2 권장 (v2)

- [ ] 키보드 전체 탐색 가능 (숫자키로 보기 선택)
- [ ] 스크린 리더 호환 (ARIA 라벨)
- [ ] 애니메이션 줄이기 옵션

---

## 8. 아이콘

### 8.1 아이콘 라이브러리

| 옵션 | 설명 | 선택 |
|------|------|------|
| Lucide React | 깔끔한 라인 아이콘 | **채택** |
| Heroicons | Tailwind 공식 | 대안 |

**설치:**
```bash
npm install lucide-react
```

### 8.2 주요 아이콘

| 용도 | 아이콘 | Lucide 이름 |
|------|--------|-------------|
| 정답 | ✓ | `Check`, `CheckCircle` |
| 오답 | ✗ | `X`, `XCircle` |
| 다음 | → | `ArrowRight`, `ChevronRight` |
| 뒤로 | ← | `ArrowLeft`, `ChevronLeft` |
| 필터 | 필터 | `Filter`, `SlidersHorizontal` |
| 홈 | 집 | `Home` |
| 닫기 | X | `X` |

### 8.3 사용 규칙

- 크기: 20px (기본), 24px (강조)
- 색상: 텍스트 색상 상속
- 버튼 내: 텍스트 왼쪽 배치, 8px 간격

---

## 9. 반응형 브레이크포인트

| 이름 | 최소 너비 | 용도 |
|------|----------|------|
| Mobile | 0px | 기본 (모바일 우선) |
| Tablet | 640px | 태블릿 |
| Desktop | 1024px | 데스크톱 |

### 9.1 주요 레이아웃 변화

| 요소 | Mobile | Desktop |
|------|--------|---------|
| 의원 사진 | 160px | 200px |
| 보기 버튼 | 1열 세로 | 2x2 그리드 |
| 컨테이너 | 100% - 32px | max-width: 480px |

---

## Decision Log 참조

| 결정 | 이유 |
|------|------|
| 듀오링고 스타일 | 사용자 요청, 지루함 방지 |
| 공식적 톤 유지 | 공공기관 앱으로서 격식 |
| Pretendard 폰트 | 한글 가독성 우수, 무료 |
| 4색 보기 | 듀오링고처럼 칼라풀하게 |
| 원형 사진 | 인물 사진에 적합, 친근함 |

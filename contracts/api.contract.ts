/**
 * API Contract: 의원얼굴퀴즈
 *
 * 이 파일은 프론트엔드와 백엔드 간의 API 계약을 정의합니다.
 * 백엔드 Pydantic 스키마와 동기화되어야 합니다.
 */

// ============================================
// 기본 타입
// ============================================

/** 지역구 */
export interface District {
  id: number;
  name: string;
  region: string;
}

/** 위원회 */
export interface Committee {
  id: number;
  name: string;
}

/** 의원 기본 정보 */
export interface Member {
  id: number;
  name: string;
  photoUrl: string;
  party: string | null;
  districtId: number;
  districtName: string;
  term: number;
}

/** 의원 상세 정보 (위원회 포함) */
export interface MemberDetail extends Member {
  committees: Committee[];
}

// ============================================
// 퀴즈 타입
// ============================================

/** 퀴즈 문제 */
export interface QuizQuestion {
  /** 정답 의원 */
  answer: Member;
  /** 4개 보기 (정답 포함, 순서 섞임) */
  options: Member[];
}

/** 퀴즈 결과 */
export interface QuizResult {
  totalQuestions: number;
  correctAnswers: number;
  accuracy: number; // 0-100
}

// ============================================
// API 응답 래퍼
// ============================================

/** 페이지네이션 메타 정보 */
export interface PaginationMeta {
  total: number;
  page: number;
  size: number;
  totalPages: number;
}

/** 단일 항목 응답 */
export interface ApiResponse<T> {
  data: T;
}

/** 목록 응답 */
export interface ApiListResponse<T> {
  data: T[];
  meta: PaginationMeta;
}

// ============================================
// API 엔드포인트 정의
// ============================================

/**
 * API 엔드포인트 목록
 *
 * Members:
 *   GET /api/members                - 의원 목록 (필터링, 페이지네이션)
 *   GET /api/members/:id            - 의원 상세
 *
 * Quiz:
 *   GET /api/quiz                   - 퀴즈 문제 생성
 *
 * Filters:
 *   GET /api/districts              - 지역구 목록
 *   GET /api/committees             - 위원회 목록
 */
export const API_ENDPOINTS = {
  members: {
    /** 의원 목록 조회 */
    list: '/api/members',
    /** 의원 상세 조회 */
    detail: (id: number) => `/api/members/${id}`,
  },
  quiz: {
    /** 퀴즈 문제 생성 */
    question: '/api/quiz',
  },
  filters: {
    /** 지역구 목록 */
    districts: '/api/districts',
    /** 위원회 목록 */
    committees: '/api/committees',
  },
} as const;

// ============================================
// 쿼리 파라미터 타입
// ============================================

/** 의원 목록 조회 쿼리 */
export interface MembersQuery {
  districtId?: number;
  committeeId?: number;
  party?: string;
  page?: number;
  size?: number;
}

/** 퀴즈 문제 생성 쿼리 */
export interface QuizQuery {
  districtId?: number;
  committeeId?: number;
}

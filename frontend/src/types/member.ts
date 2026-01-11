/**
 * 프론트엔드 타입 정의
 * contracts/api.contract.ts와 동기화
 */

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

/** 퀴즈 문제 */
export interface QuizQuestion {
  answer: Member;
  options: Member[];
}

/** 퀴즈 결과 */
export interface QuizResult {
  totalQuestions: number;
  correctAnswers: number;
  accuracy: number;
}

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

/**
 * 의원 정보 타입
 */
export interface Member {
  id: number
  name: string
  photo_url: string
  party: string
  district_id: number
  district_name: string
  term: number
}

/**
 * 지역구 정보 타입
 */
export interface District {
  id: number
  name: string
  region: string
}

/**
 * 위원회 정보 타입
 */
export interface Committee {
  id: number
  name: string
}

/**
 * 퀴즈 문제 타입
 */
export interface QuizQuestion {
  member_id: number
  photo_url: string
  options: QuizOption[]
  correct_index: number
}

/**
 * 퀴즈 선택지 타입
 */
export interface QuizOption {
  id: number
  name: string
}

/**
 * 퀴즈 결과 타입
 */
export interface QuizResult {
  total_questions: number
  correct_answers: number
  accuracy: number
  answers: QuizAnswer[]
}

/**
 * 개별 문제 답변 타입
 */
export interface QuizAnswer {
  question_index: number
  member_id: number
  member_name: string
  selected_id: number
  selected_name: string
  is_correct: boolean
}

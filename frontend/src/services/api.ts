import axios from 'axios'
import type { Member, District, Committee, QuizQuestion } from '../types'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * 의원 목록 조회
 */
export async function getMembers(params?: {
  district_id?: number
  committee_id?: number
}): Promise<Member[]> {
  const { data } = await api.get<Member[]>('/members', { params })
  return data
}

/**
 * 의원 상세 조회
 */
export async function getMember(id: number): Promise<Member> {
  const { data } = await api.get<Member>(`/members/${id}`)
  return data
}

/**
 * 지역구 목록 조회
 */
export async function getDistricts(): Promise<District[]> {
  const { data } = await api.get<District[]>('/districts')
  return data
}

/**
 * 위원회 목록 조회
 */
export async function getCommittees(): Promise<Committee[]> {
  const { data } = await api.get<Committee[]>('/committees')
  return data
}

/**
 * 퀴즈 문제 생성
 */
export async function generateQuiz(params?: {
  count?: number
  district_id?: number
  committee_id?: number
}): Promise<QuizQuestion[]> {
  const { data } = await api.get<QuizQuestion[]>('/quiz/generate', {
    params: { count: 10, ...params },
  })
  return data
}

export default api

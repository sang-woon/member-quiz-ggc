/**
 * API 서비스
 */
import axios from 'axios';
import type {
  Member,
  MemberDetail,
  District,
  Committee,
  QuizQuestion,
  ApiResponse,
  ApiListResponse,
} from '../types';

// 프로덕션에서는 같은 origin, 개발에서는 프록시 사용
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  /**
   * 의원 목록 조회
   */
  async getMembers(params?: {
    districtId?: number;
    committeeId?: number;
    party?: string;
    page?: number;
    size?: number;
  }): Promise<ApiListResponse<Member>> {
    const { data } = await client.get<ApiListResponse<Member>>('/members', { params });
    return data;
  },

  /**
   * 의원 상세 조회
   */
  async getMember(id: number): Promise<ApiResponse<MemberDetail>> {
    const { data } = await client.get<ApiResponse<MemberDetail>>(`/members/${id}`);
    return data;
  },

  /**
   * 지역구 목록 조회
   */
  async getDistricts(): Promise<ApiResponse<District[]>> {
    const { data } = await client.get<ApiResponse<District[]>>('/districts');
    return data;
  },

  /**
   * 위원회 목록 조회
   */
  async getCommittees(): Promise<ApiResponse<Committee[]>> {
    const { data } = await client.get<ApiResponse<Committee[]>>('/committees');
    return data;
  },

  /**
   * 퀴즈 문제 생성
   */
  async getQuizQuestion(params?: {
    districtId?: number;
    committeeId?: number;
  }): Promise<QuizQuestion> {
    const { data } = await client.get<QuizQuestion>('/quiz', { params });
    return data;
  },
};

export default client;

/**
 * 필터 API 목 핸들러
 */
import { http, HttpResponse } from 'msw';
import { mockDistricts, mockCommittees } from '../data/members';
import type { ApiResponse, District, Committee } from '../../types';

export const filterHandlers = [
  // 지역구 목록 조회
  http.get('/api/districts', () => {
    const response: ApiResponse<District[]> = {
      data: mockDistricts,
    };
    return HttpResponse.json(response);
  }),

  // 위원회 목록 조회
  http.get('/api/committees', () => {
    const response: ApiResponse<Committee[]> = {
      data: mockCommittees,
    };
    return HttpResponse.json(response);
  }),
];

/**
 * 퀴즈 API 목 핸들러
 */
import { http, HttpResponse } from 'msw';
import { mockMembers, getRandomQuizQuestion } from '../data/members';
import type { QuizQuestion } from '../../types';

export const quizHandlers = [
  // 퀴즈 문제 생성
  http.get('/api/quiz', ({ request }) => {
    const url = new URL(request.url);
    const districtId = url.searchParams.get('districtId');
    const committeeId = url.searchParams.get('committeeId');

    let members = [...mockMembers];

    // 지역구 필터
    if (districtId) {
      members = members.filter(m => m.districtId === parseInt(districtId));
    }

    // 최소 4명이 필요
    if (members.length < 4) {
      members = mockMembers;
    }

    // 랜덤하게 섞기
    const shuffled = members.sort(() => Math.random() - 0.5);
    const answer = shuffled[0];
    const options = shuffled.slice(0, 4);

    const quizQuestion: QuizQuestion = {
      answer,
      options,
    };

    return HttpResponse.json(quizQuestion);
  }),
];

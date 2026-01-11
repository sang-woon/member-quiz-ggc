/**
 * 의원 API 목 핸들러
 */
import { http, HttpResponse } from 'msw';
import { mockMembers, mockDistricts } from '../data/members';
import type { ApiListResponse, ApiResponse, MemberDetail } from '../../types';

export const memberHandlers = [
  // 의원 목록 조회
  http.get('/api/members', ({ request }) => {
    const url = new URL(request.url);
    const districtId = url.searchParams.get('districtId');
    const committeeId = url.searchParams.get('committeeId');
    const page = parseInt(url.searchParams.get('page') || '1');
    const size = parseInt(url.searchParams.get('size') || '20');

    let filtered = [...mockMembers];

    if (districtId) {
      filtered = filtered.filter(m => m.districtId === parseInt(districtId));
    }

    // 페이지네이션
    const start = (page - 1) * size;
    const end = start + size;
    const paginated = filtered.slice(start, end);

    const response: ApiListResponse<typeof mockMembers[0]> = {
      data: paginated,
      meta: {
        total: filtered.length,
        page,
        size,
        totalPages: Math.ceil(filtered.length / size),
      },
    };

    return HttpResponse.json(response);
  }),

  // 의원 상세 조회
  http.get('/api/members/:id', ({ params }) => {
    const id = parseInt(params.id as string);
    const member = mockMembers.find(m => m.id === id);

    if (!member) {
      return HttpResponse.json(
        { error: '의원을 찾을 수 없습니다.' },
        { status: 404 }
      );
    }

    const memberDetail: MemberDetail = {
      ...member,
      committees: [{ id: 1, name: '운영위원회' }],
    };

    const response: ApiResponse<MemberDetail> = {
      data: memberDetail,
    };

    return HttpResponse.json(response);
  }),
];

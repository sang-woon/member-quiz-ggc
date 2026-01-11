/**
 * 테스트용 목 데이터
 */
import type { Member, District, Committee, QuizQuestion } from '../../types';

export const mockDistricts: District[] = [
  { id: 1, name: '수원시갑', region: '수원권' },
  { id: 2, name: '성남시분당갑', region: '성남권' },
  { id: 3, name: '비례대표', region: '비례대표' },
];

export const mockCommittees: Committee[] = [
  { id: 1, name: '운영위원회' },
  { id: 2, name: '기획재정위원회' },
  { id: 3, name: '행정안전위원회' },
];

export const mockMembers: Member[] = [
  {
    id: 1,
    name: '김철수',
    photoUrl: '/images/members/김철수.jpg',
    party: '더불어민주당',
    districtId: 1,
    districtName: '수원시갑',
    term: 11,
  },
  {
    id: 2,
    name: '이영희',
    photoUrl: '/images/members/이영희.jpg',
    party: '국민의힘',
    districtId: 2,
    districtName: '성남시분당갑',
    term: 11,
  },
  {
    id: 3,
    name: '박지성',
    photoUrl: '/images/members/박지성.jpg',
    party: '더불어민주당',
    districtId: 1,
    districtName: '수원시갑',
    term: 11,
  },
  {
    id: 4,
    name: '최유리',
    photoUrl: '/images/members/최유리.jpg',
    party: '국민의힘',
    districtId: 3,
    districtName: '비례대표',
    term: 11,
  },
  {
    id: 5,
    name: '정민수',
    photoUrl: '/images/members/정민수.jpg',
    party: '더불어민주당',
    districtId: 2,
    districtName: '성남시분당갑',
    term: 11,
  },
];

export const mockQuizQuestion: QuizQuestion = {
  answer: mockMembers[0],
  options: [mockMembers[0], mockMembers[1], mockMembers[2], mockMembers[3]],
};

export function getRandomQuizQuestion(): QuizQuestion {
  const shuffled = [...mockMembers].sort(() => Math.random() - 0.5);
  const answer = shuffled[0];
  const options = shuffled.slice(0, 4);
  return { answer, options };
}

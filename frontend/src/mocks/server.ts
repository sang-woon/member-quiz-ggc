/**
 * 테스트용 MSW 서버 설정
 * Vitest에서 사용
 */
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);

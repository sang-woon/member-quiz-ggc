/**
 * Vitest 테스트 설정
 */
import { afterAll, afterEach, beforeAll } from 'vitest';
import { server } from '../mocks/server';
import '@testing-library/jest-dom/vitest';

// MSW 서버 시작/종료
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

/**
 * QuizPage 컴포넌트 테스트 (RED 상태 - 컴포넌트 미구현)
 */
import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
// TODO: 컴포넌트 구현 후 import
// import { QuizPage } from '@/pages/QuizPage';

describe('QuizPage', () => {
  it.skip('퀴즈 문제를 로드한다', async () => {
    // render(<QuizPage />);
    // await waitFor(() => {
    //   expect(screen.getByRole('img')).toBeInTheDocument();
    // });
  });

  it.skip('문제 번호를 표시한다 (1/10)', () => {
    // render(<QuizPage />);
    // expect(screen.getByText(/1.*\/.*10/)).toBeInTheDocument();
  });

  it.skip('진행률 바를 표시한다', () => {
    // render(<QuizPage />);
    // expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it.skip('정답 선택 시 다음 문제로 넘어간다', async () => {
    // const user = userEvent.setup();
    // render(<QuizPage />);
    //
    // // 첫 번째 문제 답변
    // const option = await screen.findByRole('button', { name: /김철수/i });
    // await user.click(option);
    //
    // // 다음 문제로 전환
    // await waitFor(() => {
    //   expect(screen.getByText(/2.*\/.*10/)).toBeInTheDocument();
    // });
  });

  it.skip('10문제 완료 후 결과 화면으로 이동한다', async () => {
    // TODO: 10문제 완료 후 라우팅 테스트
  });

  it.skip('오답 선택 시 정답 정보를 표시한다', async () => {
    // TODO: 오답 시 정답 표시 테스트
  });

  it.skip('로딩 중 스피너를 표시한다', () => {
    // render(<QuizPage />);
    // expect(screen.getByText(/로딩/i)).toBeInTheDocument();
  });
});

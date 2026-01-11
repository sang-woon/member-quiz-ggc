/**
 * ResultPage 컴포넌트 테스트 (RED 상태 - 컴포넌트 미구현)
 */
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
// TODO: 컴포넌트 구현 후 import
// import { ResultPage } from '@/pages/ResultPage';

describe('ResultPage', () => {
  const mockResult = {
    totalQuestions: 10,
    correctAnswers: 8,
    accuracy: 80,
  };

  it.skip('점수를 표시한다 (X / 10)', () => {
    // render(<ResultPage result={mockResult} />);
    // expect(screen.getByText(/8.*\/.*10/)).toBeInTheDocument();
  });

  it.skip('정답률을 표시한다', () => {
    // render(<ResultPage result={mockResult} />);
    // expect(screen.getByText(/80%/)).toBeInTheDocument();
  });

  it.skip('80% 이상일 때 축하 메시지를 표시한다', () => {
    // render(<ResultPage result={mockResult} />);
    // expect(screen.getByText(/훌륭합니다/i)).toBeInTheDocument();
  });

  it.skip('80% 미만일 때 격려 메시지를 표시한다', () => {
    // const lowResult = { ...mockResult, correctAnswers: 5, accuracy: 50 };
    // render(<ResultPage result={lowResult} />);
    // expect(screen.getByText(/더 연습/i)).toBeInTheDocument();
  });

  it.skip('"다시 도전" 버튼을 표시한다', () => {
    // render(<ResultPage result={mockResult} />);
    // expect(screen.getByRole('button', { name: /다시 도전/i })).toBeInTheDocument();
  });

  it.skip('"메인으로" 버튼을 표시한다', () => {
    // render(<ResultPage result={mockResult} />);
    // expect(screen.getByRole('button', { name: /메인으로/i })).toBeInTheDocument();
  });

  it.skip('"다시 도전" 클릭 시 퀴즈 페이지로 이동한다', async () => {
    // TODO: 라우팅 테스트
  });

  it.skip('"메인으로" 클릭 시 메인 페이지로 이동한다', async () => {
    // TODO: 라우팅 테스트
  });
});

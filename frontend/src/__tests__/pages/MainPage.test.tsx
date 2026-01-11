/**
 * MainPage 컴포넌트 테스트 (RED 상태 - 컴포넌트 미구현)
 */
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
// TODO: 컴포넌트 구현 후 import
// import { MainPage } from '@/pages/MainPage';

describe('MainPage', () => {
  it.skip('앱 타이틀을 표시한다', () => {
    // render(<MainPage />);
    // expect(screen.getByText(/의원 얼굴 퀴즈/i)).toBeInTheDocument();
  });

  it.skip('"전체 퀴즈 시작" 버튼을 표시한다', () => {
    // render(<MainPage />);
    // expect(screen.getByRole('button', { name: /전체 퀴즈 시작/i })).toBeInTheDocument();
  });

  it.skip('지역구 필터 드롭다운을 표시한다', () => {
    // render(<MainPage />);
    // expect(screen.getByLabelText(/지역구/i)).toBeInTheDocument();
  });

  it.skip('위원회 필터 드롭다운을 표시한다', () => {
    // render(<MainPage />);
    // expect(screen.getByLabelText(/위원회/i)).toBeInTheDocument();
  });

  it.skip('필터 선택 후 "선택 퀴즈 시작" 버튼이 활성화된다', async () => {
    // const user = userEvent.setup();
    // render(<MainPage />);
    //
    // const districtSelect = screen.getByLabelText(/지역구/i);
    // await user.selectOptions(districtSelect, '1');
    //
    // const startButton = screen.getByRole('button', { name: /선택 퀴즈 시작/i });
    // expect(startButton).not.toBeDisabled();
  });

  it.skip('"전체 퀴즈 시작" 클릭 시 퀴즈 페이지로 이동한다', async () => {
    // TODO: 라우팅 테스트
  });

  it.skip('반응형 레이아웃이 적용된다', () => {
    // TODO: 반응형 테스트
  });
});

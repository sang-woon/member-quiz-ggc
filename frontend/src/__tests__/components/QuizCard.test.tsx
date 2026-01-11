/**
 * QuizCard 컴포넌트 테스트 (RED 상태 - 컴포넌트 미구현)
 */
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
// TODO: 컴포넌트 구현 후 import
// import { QuizCard } from '@/components/quiz/QuizCard';
import { mockQuizQuestion } from '../../mocks/data/members';

describe('QuizCard', () => {
  const mockOnAnswer = vi.fn();

  it.skip('의원 사진을 표시한다', () => {
    // TODO: 컴포넌트 구현 후 테스트
    // render(
    //   <QuizCard
    //     question={mockQuizQuestion}
    //     onAnswer={mockOnAnswer}
    //   />
    // );
    // expect(screen.getByRole('img')).toBeInTheDocument();
    // expect(screen.getByRole('img')).toHaveAttribute('src', mockQuizQuestion.answer.photoUrl);
  });

  it.skip('4개의 보기 버튼을 표시한다', () => {
    // render(
    //   <QuizCard
    //     question={mockQuizQuestion}
    //     onAnswer={mockOnAnswer}
    //   />
    // );
    // const buttons = screen.getAllByRole('button');
    // expect(buttons).toHaveLength(4);
  });

  it.skip('각 보기에 의원 이름이 표시된다', () => {
    // render(
    //   <QuizCard
    //     question={mockQuizQuestion}
    //     onAnswer={mockOnAnswer}
    //   />
    // );
    // mockQuizQuestion.options.forEach(option => {
    //   expect(screen.getByText(option.name)).toBeInTheDocument();
    // });
  });

  it.skip('보기 클릭 시 onAnswer 콜백이 호출된다', async () => {
    // const user = userEvent.setup();
    // render(
    //   <QuizCard
    //     question={mockQuizQuestion}
    //     onAnswer={mockOnAnswer}
    //   />
    // );
    //
    // const firstOption = screen.getByText(mockQuizQuestion.options[0].name);
    // await user.click(firstOption);
    //
    // expect(mockOnAnswer).toHaveBeenCalledWith(mockQuizQuestion.options[0].id);
  });

  it.skip('정답 클릭 시 정답 애니메이션이 표시된다', async () => {
    // TODO: 정답 애니메이션 테스트
  });

  it.skip('오답 클릭 시 오답 애니메이션이 표시된다', async () => {
    // TODO: 오답 애니메이션 테스트
  });

  it.skip('답변 후 다음 문제로 넘어가기 전 정답을 보여준다', () => {
    // TODO: 정답 표시 테스트
  });
});

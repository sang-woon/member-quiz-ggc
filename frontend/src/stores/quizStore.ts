/**
 * 퀴즈 상태 스토어 (현재 미사용 - 추후 확장용)
 */
import { create } from 'zustand';
import type { QuizQuestion, QuizResult } from '../types';

interface QuizAnswer {
  questionIndex: number;
  memberId: number;
  memberName: string;
  selectedId: number;
  selectedName: string;
  isCorrect: boolean;
}

interface QuizState {
  questions: QuizQuestion[];
  currentIndex: number;
  answers: QuizAnswer[];
  districtId: number | null;
  committeeId: number | null;

  setQuestions: (questions: QuizQuestion[]) => void;
  setCurrentIndex: (index: number) => void;
  addAnswer: (answer: QuizAnswer) => void;
  setFilter: (districtId: number | null, committeeId: number | null) => void;
  reset: () => void;
  getResult: () => QuizResult;
}

const initialState = {
  questions: [] as QuizQuestion[],
  currentIndex: 0,
  answers: [] as QuizAnswer[],
  districtId: null as number | null,
  committeeId: null as number | null,
};

export const useQuizStore = create<QuizState>((set, get) => ({
  ...initialState,

  setQuestions: (questions) => set({ questions }),
  setCurrentIndex: (index) => set({ currentIndex: index }),
  addAnswer: (answer) =>
    set((state) => ({
      answers: [...state.answers, answer],
    })),
  setFilter: (districtId, committeeId) => set({ districtId, committeeId }),
  reset: () => set(initialState),

  getResult: () => {
    const { questions, answers } = get();
    const correctAnswers = answers.filter((a) => a.isCorrect).length;
    return {
      totalQuestions: questions.length,
      correctAnswers,
      accuracy:
        questions.length > 0 ? (correctAnswers / questions.length) * 100 : 0,
    };
  },
}));

import { create } from 'zustand'
import type { QuizQuestion, QuizAnswer, QuizResult } from '../types'

interface QuizState {
  // 상태
  questions: QuizQuestion[]
  currentIndex: number
  answers: QuizAnswer[]
  isLoading: boolean
  error: string | null

  // 필터
  districtId: number | null
  committeeId: number | null

  // 액션
  setQuestions: (questions: QuizQuestion[]) => void
  setCurrentIndex: (index: number) => void
  addAnswer: (answer: QuizAnswer) => void
  setFilter: (districtId: number | null, committeeId: number | null) => void
  reset: () => void
  getResult: () => QuizResult
}

const initialState = {
  questions: [],
  currentIndex: 0,
  answers: [],
  isLoading: false,
  error: null,
  districtId: null,
  committeeId: null,
}

export const useQuizStore = create<QuizState>((set, get) => ({
  ...initialState,

  setQuestions: (questions) => set({ questions }),

  setCurrentIndex: (index) => set({ currentIndex: index }),

  addAnswer: (answer) => set((state) => ({
    answers: [...state.answers, answer],
  })),

  setFilter: (districtId, committeeId) => set({ districtId, committeeId }),

  reset: () => set(initialState),

  getResult: () => {
    const { questions, answers } = get()
    const correctAnswers = answers.filter((a) => a.is_correct).length
    return {
      total_questions: questions.length,
      correct_answers: correctAnswers,
      accuracy: questions.length > 0 ? (correctAnswers / questions.length) * 100 : 0,
      answers,
    }
  },
}))

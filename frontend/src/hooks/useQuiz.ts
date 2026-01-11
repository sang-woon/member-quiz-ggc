import { useQuery } from '@tanstack/react-query'
import { generateQuiz } from '../services/api'
import { useQuizStore } from '../stores/quizStore'

interface UseQuizOptions {
  count?: number
  districtId?: number | null
  committeeId?: number | null
}

export function useQuiz(options: UseQuizOptions = {}) {
  const { count = 10, districtId, committeeId } = options
  const { setQuestions, questions, currentIndex, answers, addAnswer, reset, getResult } = useQuizStore()

  const query = useQuery({
    queryKey: ['quiz', count, districtId, committeeId],
    queryFn: () => generateQuiz({
      count,
      district_id: districtId ?? undefined,
      committee_id: committeeId ?? undefined,
    }),
    enabled: false, // 수동으로 트리거
  })

  const startQuiz = async () => {
    reset()
    const result = await query.refetch()
    if (result.data) {
      setQuestions(result.data)
    }
  }

  const currentQuestion = questions[currentIndex]
  const isComplete = currentIndex >= questions.length && questions.length > 0
  const progress = questions.length > 0 ? (currentIndex / questions.length) * 100 : 0

  return {
    // 상태
    questions,
    currentQuestion,
    currentIndex,
    answers,
    isLoading: query.isLoading,
    error: query.error,
    isComplete,
    progress,

    // 액션
    startQuiz,
    addAnswer,
    getResult,
    reset,
  }
}

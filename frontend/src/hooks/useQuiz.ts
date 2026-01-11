/**
 * 퀴즈 훅 (현재 미사용 - 추후 확장용)
 */
import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';
import { useQuizStore } from '../stores/quizStore';

interface UseQuizOptions {
  districtId?: number | null;
  committeeId?: number | null;
}

export function useQuiz(options: UseQuizOptions = {}) {
  const { districtId, committeeId } = options;
  const store = useQuizStore();

  const query = useQuery({
    queryKey: ['quiz', districtId, committeeId],
    queryFn: () =>
      api.getQuizQuestion({
        districtId: districtId ?? undefined,
        committeeId: committeeId ?? undefined,
      }),
    enabled: false,
  });

  const startQuiz = async () => {
    store.reset();
    await query.refetch();
  };

  return {
    currentQuestion: query.data,
    isLoading: query.isLoading,
    error: query.error,
    startQuiz,
    reset: store.reset,
  };
}

/**
 * 퀴즈 페이지
 */
import { useState, useCallback } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { motion, AnimatePresence } from 'framer-motion';
import { QuizCard, ProgressBar } from '../components/quiz';
import { Button } from '../components/common';
import { api } from '../services/api';
import type { QuizResult } from '../types';

const TOTAL_QUESTIONS = 10;

export function QuizPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const districtId = searchParams.get('districtId');
  const committeeId = searchParams.get('committeeId');

  const [currentQuestion, setCurrentQuestion] = useState(1);
  const [correctAnswers, setCorrectAnswers] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const [questionKey, setQuestionKey] = useState(0);

  // 퀴즈 문제 가져오기
  const { data: question, isLoading, refetch } = useQuery({
    queryKey: ['quiz', questionKey, districtId, committeeId],
    queryFn: () =>
      api.getQuizQuestion({
        districtId: districtId ? parseInt(districtId) : undefined,
        committeeId: committeeId ? parseInt(committeeId) : undefined,
      }),
    staleTime: 0,
    gcTime: 0,
  });

  const handleAnswer = useCallback((memberId: number) => {
    if (!question || selectedAnswer !== null) return;

    const correct = memberId === question.answer.id;
    setSelectedAnswer(memberId);
    setIsCorrect(correct);

    if (correct) {
      setCorrectAnswers((prev) => prev + 1);
    }

    // 1.5초 후 다음 문제로
    setTimeout(() => {
      if (currentQuestion >= TOTAL_QUESTIONS) {
        // 결과 페이지로 이동
        const result: QuizResult = {
          totalQuestions: TOTAL_QUESTIONS,
          correctAnswers: correct ? correctAnswers + 1 : correctAnswers,
          accuracy: ((correct ? correctAnswers + 1 : correctAnswers) / TOTAL_QUESTIONS) * 100,
        };
        navigate('/result', { state: { result } });
      } else {
        // 다음 문제
        setCurrentQuestion((prev) => prev + 1);
        setSelectedAnswer(null);
        setIsCorrect(null);
        setQuestionKey((prev) => prev + 1);
      }
    }, 1500);
  }, [question, selectedAnswer, currentQuestion, correctAnswers, navigate]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
          className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full"
        />
      </div>
    );
  }

  if (!question) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen p-4">
        <p className="text-lg text-neutral-muted mb-4">
          퀴즈를 불러올 수 없습니다.
        </p>
        <Button onClick={() => refetch()}>다시 시도</Button>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-4 py-8">
      <div className="max-w-md mx-auto">
        {/* 진행률 */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <ProgressBar current={currentQuestion} total={TOTAL_QUESTIONS} />
        </motion.div>

        {/* 퀴즈 카드 */}
        <AnimatePresence mode="wait">
          <motion.div
            key={questionKey}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            transition={{ duration: 0.3 }}
          >
            <QuizCard
              question={question}
              onAnswer={handleAnswer}
              selectedAnswer={selectedAnswer}
              isCorrect={isCorrect}
            />
          </motion.div>
        </AnimatePresence>

        {/* 현재 점수 */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-8 text-center text-sm text-neutral-muted"
        >
          현재 점수: {correctAnswers} / {currentQuestion - (selectedAnswer !== null ? 0 : 1)}
        </motion.div>
      </div>
    </div>
  );
}

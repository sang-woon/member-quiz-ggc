/**
 * 결과 페이지
 */
import { useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button } from '../components/common';
import type { QuizResult } from '../types';

export function ResultPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const result = location.state?.result as QuizResult | undefined;

  // 결과 없이 직접 접근한 경우
  if (!result) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen p-4">
        <p className="text-lg text-neutral-muted mb-4">
          결과 데이터가 없습니다.
        </p>
        <Button onClick={() => navigate('/')}>메인으로</Button>
      </div>
    );
  }

  const { totalQuestions, correctAnswers, accuracy } = result;
  const isExcellent = accuracy >= 80;

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ type: 'spring', stiffness: 200, damping: 15 }}
        className={`
          w-40 h-40 rounded-full
          flex items-center justify-center
          text-6xl font-bold text-white
          ${isExcellent ? 'bg-success' : 'bg-secondary'}
          shadow-xl mb-8
        `}
      >
        {isExcellent ? '🎉' : '💪'}
      </motion.div>

      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="text-3xl font-bold text-neutral-text mb-2"
      >
        {isExcellent ? '훌륭합니다!' : '더 연습해보세요!'}
      </motion.h1>

      <motion.p
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="text-lg text-neutral-muted mb-8"
      >
        {isExcellent
          ? '경기도의회 의원을 잘 알고 계시네요!'
          : '조금만 더 연습하면 완벽해질 거예요!'}
      </motion.p>

      {/* 점수 표시 */}
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.4 }}
        className="bg-white rounded-2xl p-6 shadow-md mb-8 text-center"
      >
        <div className="text-5xl font-bold text-primary mb-2">
          {correctAnswers} / {totalQuestions}
        </div>
        <div className="text-2xl font-semibold text-neutral-text">
          정답률 {Math.round(accuracy)}%
        </div>
        <div className="mt-4 h-4 bg-neutral-100 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${accuracy}%` }}
            transition={{ delay: 0.6, duration: 0.8, ease: 'easeOut' }}
            className={`h-full rounded-full ${isExcellent ? 'bg-success' : 'bg-secondary'}`}
          />
        </div>
      </motion.div>

      {/* 버튼들 */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="flex flex-col gap-3 w-full max-w-xs"
      >
        <Button onClick={() => navigate('/quiz')} size="lg" fullWidth>
          다시 도전
        </Button>
        <Button
          onClick={() => navigate('/')}
          variant="outline"
          size="lg"
          fullWidth
        >
          메인으로
        </Button>
      </motion.div>
    </div>
  );
}

/**
 * 퀴즈 카드 컴포넌트
 */
import { motion, AnimatePresence } from 'framer-motion';
import type { Member, QuizQuestion } from '../../types';
import { OptimizedImage } from '../common/OptimizedImage';

interface QuizCardProps {
  question: QuizQuestion;
  onAnswer: (memberId: number) => void;
  selectedAnswer: number | null;
  isCorrect: boolean | null;
}

export function QuizCard({
  question,
  onAnswer,
  selectedAnswer,
  isCorrect,
}: QuizCardProps) {
  const { answer, options } = question;

  const getButtonStyle = (option: Member) => {
    if (selectedAnswer === null) {
      return 'bg-white border-2 border-neutral-border hover:border-primary hover:bg-primary/5';
    }

    if (option.id === answer.id) {
      return 'bg-success border-2 border-success text-white';
    }

    if (option.id === selectedAnswer && !isCorrect) {
      return 'bg-error border-2 border-error text-white';
    }

    return 'bg-neutral-50 border-2 border-neutral-border opacity-50';
  };

  return (
    <div className="w-full max-w-md mx-auto">
      {/* 의원 사진 */}
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="flex justify-center mb-8"
      >
        <div className="relative">
          <motion.div
            animate={
              selectedAnswer !== null
                ? isCorrect
                  ? { scale: [1, 1.1, 1] }
                  : { x: [-5, 5, -5, 5, 0] }
                : {}
            }
            transition={{ duration: 0.3 }}
            className="w-48 h-48 md:w-56 md:h-56 rounded-full overflow-hidden border-4 border-white shadow-xl"
          >
            <OptimizedImage
              src={answer.photoUrl}
              alt="의원 사진"
              className="w-full h-full"
            />
          </motion.div>
          {/* 결과 표시 배지 */}
          <AnimatePresence>
            {selectedAnswer !== null && (
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                exit={{ scale: 0 }}
                className={`
                  absolute -bottom-2 -right-2
                  w-12 h-12 rounded-full
                  flex items-center justify-center
                  text-2xl font-bold
                  ${isCorrect ? 'bg-success' : 'bg-error'}
                  text-white shadow-lg
                `}
              >
                {isCorrect ? 'O' : 'X'}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.div>

      {/* 질문 */}
      <h2 className="text-xl font-bold text-center text-neutral-text mb-6">
        이 의원의 이름은?
      </h2>

      {/* 보기 버튼들 */}
      <div className="grid grid-cols-2 gap-3">
        {options.map((option, index) => (
          <motion.button
            key={option.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            onClick={() => selectedAnswer === null && onAnswer(option.id)}
            disabled={selectedAnswer !== null}
            className={`
              ${getButtonStyle(option)}
              px-4 py-4
              rounded-xl
              font-semibold
              transition-all duration-200
              ${selectedAnswer === null ? 'cursor-pointer' : 'cursor-default'}
            `}
          >
            {option.name}
          </motion.button>
        ))}
      </div>

      {/* 정답 정보 (오답 시 표시) */}
      <AnimatePresence>
        {selectedAnswer !== null && !isCorrect && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="mt-6 p-4 bg-primary/10 rounded-xl text-center"
          >
            <p className="text-neutral-muted text-sm">정답</p>
            <p className="text-lg font-bold text-primary">{answer.name}</p>
            <p className="text-sm text-neutral-muted">
              {answer.districtName} / {answer.party}
            </p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

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

// 정당별 색상
const partyColors: Record<string, string> = {
  '더불어민주당': 'bg-blue-500',
  '국민의힘': 'bg-red-500',
  '정의당': 'bg-yellow-500',
  '무소속': 'bg-gray-500',
};

function getPartyColor(party: string | null): string {
  if (!party) return 'bg-gray-400';
  return partyColors[party] || 'bg-gray-400';
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
    <div className="w-full max-w-lg mx-auto">
      {/* 의원 사진 */}
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="flex justify-center mb-6"
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
            className="w-40 h-40 md:w-48 md:h-48 rounded-full overflow-hidden border-4 border-white shadow-xl"
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
                  w-10 h-10 rounded-full
                  flex items-center justify-center
                  text-xl font-bold
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
      <h2 className="text-lg font-bold text-center text-neutral-text mb-4">
        이 의원의 이름은?
      </h2>

      {/* 보기 버튼들 */}
      <div className="grid grid-cols-2 gap-2">
        {options.map((option, index) => (
          <motion.button
            key={option.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            onClick={() => selectedAnswer === null && onAnswer(option.id)}
            disabled={selectedAnswer !== null}
            className={`
              ${getButtonStyle(option)}
              px-3 py-3
              rounded-xl
              transition-all duration-200
              ${selectedAnswer === null ? 'cursor-pointer' : 'cursor-default'}
            `}
          >
            <div className="flex flex-col items-center gap-1">
              <span className="font-semibold text-base">{option.name}</span>
              {/* 정당 배지 */}
              <span className={`
                text-xs px-2 py-0.5 rounded-full text-white
                ${selectedAnswer === null ? getPartyColor(option.party) :
                  option.id === answer.id ? 'bg-white/30' :
                  option.id === selectedAnswer ? 'bg-white/30' : 'bg-gray-400'}
              `}>
                {option.party || '무소속'}
              </span>
            </div>
          </motion.button>
        ))}
      </div>

      {/* 정답 정보 (답변 후 항상 표시) */}
      <AnimatePresence>
        {selectedAnswer !== null && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className={`mt-4 p-4 rounded-xl ${isCorrect ? 'bg-success/10' : 'bg-primary/10'}`}
          >
            <div className="text-center">
              <p className="text-neutral-muted text-xs mb-1">
                {isCorrect ? '정답입니다!' : '정답'}
              </p>
              <p className="text-xl font-bold text-primary mb-2">{answer.name}</p>

              {/* 상세 정보 */}
              <div className="flex flex-wrap justify-center gap-2 text-sm">
                {/* 정당 */}
                <span className={`px-2 py-1 rounded-full text-white ${getPartyColor(answer.party)}`}>
                  {answer.party || '무소속'}
                </span>
                {/* 지역구 */}
                <span className="px-2 py-1 rounded-full bg-neutral-200 text-neutral-700">
                  {answer.districtName}
                </span>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

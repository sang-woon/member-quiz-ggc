/**
 * 메인 페이지
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { Button, FilterDropdown } from '../components/common';
import { api } from '../services/api';

export function MainPage() {
  const navigate = useNavigate();
  const [districtId, setDistrictId] = useState<number | null>(null);
  const [committeeId, setCommitteeId] = useState<number | null>(null);

  // 지역구 목록 조회
  const { data: districtsData } = useQuery({
    queryKey: ['districts'],
    queryFn: api.getDistricts,
  });

  // 위원회 목록 조회
  const { data: committeesData } = useQuery({
    queryKey: ['committees'],
    queryFn: api.getCommittees,
  });

  const districts = districtsData?.data ?? [];
  const committees = committeesData?.data ?? [];

  const handleStartQuiz = (filtered: boolean = false) => {
    const params = new URLSearchParams();
    if (filtered) {
      if (districtId) params.set('districtId', districtId.toString());
      if (committeeId) params.set('committeeId', committeeId.toString());
    }
    navigate(`/quiz${params.toString() ? '?' + params.toString() : ''}`);
  };

  const hasFilter = districtId !== null || committeeId !== null;

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <h1 className="text-4xl md:text-5xl font-bold text-neutral-text mb-4">
          의원 얼굴 퀴즈
        </h1>
        <p className="text-lg text-neutral-muted">
          경기도의회 11대 의원 얼굴 맞추기
        </p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="w-full max-w-md space-y-6"
      >
        {/* 전체 퀴즈 시작 버튼 */}
        <Button
          onClick={() => handleStartQuiz(false)}
          size="lg"
          fullWidth
        >
          전체 퀴즈 시작
        </Button>

        {/* 구분선 */}
        <div className="flex items-center gap-4">
          <div className="flex-1 h-px bg-neutral-border" />
          <span className="text-sm text-neutral-muted">또는</span>
          <div className="flex-1 h-px bg-neutral-border" />
        </div>

        {/* 필터 섹션 */}
        <div className="bg-white rounded-2xl p-6 shadow-md space-y-4">
          <h2 className="text-lg font-semibold text-neutral-text">
            범위 선택
          </h2>

          <FilterDropdown
            label="지역구"
            options={districts}
            value={districtId}
            onChange={setDistrictId}
          />

          <FilterDropdown
            label="위원회"
            options={committees}
            value={committeeId}
            onChange={setCommitteeId}
          />

          <Button
            onClick={() => handleStartQuiz(true)}
            variant={hasFilter ? 'primary' : 'outline'}
            fullWidth
            disabled={!hasFilter}
          >
            {hasFilter ? '선택 범위로 퀴즈 시작' : '범위를 선택하세요'}
          </Button>
        </div>

        {/* 통계 정보 */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="text-center text-sm text-neutral-muted"
        >
          총 155명의 의원 데이터
        </motion.div>
      </motion.div>
    </div>
  );
}

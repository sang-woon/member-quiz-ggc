/**
 * 최적화된 이미지 컴포넌트
 * - 로딩 상태 표시
 * - lazy loading
 * - 에러 상태 처리
 */
import { useState } from 'react';

interface OptimizedImageProps {
  src: string;
  alt: string;
  className?: string;
}

export function OptimizedImage({
  src,
  alt,
  className = '',
}: OptimizedImageProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);

  return (
    <div className={`relative ${className}`}>
      {/* 로딩 플레이스홀더 */}
      {isLoading && !hasError && (
        <div className="absolute inset-0 flex items-center justify-center bg-neutral-100 animate-pulse rounded-full">
          <svg
            className="w-10 h-10 text-neutral-300 animate-spin"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        </div>
      )}

      {/* 에러 플레이스홀더 */}
      {hasError && (
        <div className="absolute inset-0 flex items-center justify-center bg-neutral-100 rounded-full">
          <svg
            className="w-16 h-16 text-neutral-300"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1}
              d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
            />
          </svg>
        </div>
      )}

      {/* 실제 이미지 */}
      <img
        src={src}
        alt={alt}
        loading="lazy"
        decoding="async"
        onLoad={() => setIsLoading(false)}
        onError={() => {
          setIsLoading(false);
          setHasError(true);
        }}
        className={`w-full h-full object-cover transition-opacity duration-200 ${
          isLoading || hasError ? 'opacity-0' : 'opacity-100'
        }`}
      />
    </div>
  );
}

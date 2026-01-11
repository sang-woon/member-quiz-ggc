/**
 * 최적화된 이미지 컴포넌트
 * - wsrv.nl 프록시를 통한 이미지 리사이징
 * - 로딩 상태 표시
 * - lazy loading
 */
import { useState } from 'react';

interface OptimizedImageProps {
  src: string;
  alt: string;
  width?: number;
  height?: number;
  className?: string;
}

/**
 * 이미지 URL을 최적화된 프록시 URL로 변환
 */
function getOptimizedUrl(src: string, width: number, height: number): string {
  // wsrv.nl 이미지 프록시 사용 (무료, 빠름)
  const encodedUrl = encodeURIComponent(src);
  return `https://wsrv.nl/?url=${encodedUrl}&w=${width}&h=${height}&fit=cover&q=80`;
}

export function OptimizedImage({
  src,
  alt,
  width = 224,
  height = 224,
  className = '',
}: OptimizedImageProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);

  const optimizedSrc = getOptimizedUrl(src, width, height);

  return (
    <div className={`relative ${className}`}>
      {/* 로딩 플레이스홀더 */}
      {isLoading && !hasError && (
        <div className="absolute inset-0 flex items-center justify-center bg-neutral-100 animate-pulse">
          <svg
            className="w-12 h-12 text-neutral-300 animate-spin"
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
        <div className="absolute inset-0 flex items-center justify-center bg-neutral-100">
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
        src={optimizedSrc}
        alt={alt}
        loading="lazy"
        onLoad={() => setIsLoading(false)}
        onError={() => {
          setIsLoading(false);
          setHasError(true);
        }}
        className={`w-full h-full object-cover transition-opacity duration-300 ${
          isLoading || hasError ? 'opacity-0' : 'opacity-100'
        }`}
      />
    </div>
  );
}

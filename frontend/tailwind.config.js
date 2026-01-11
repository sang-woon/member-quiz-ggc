/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // 듀오링고 스타일 + 공식 톤
        primary: {
          DEFAULT: '#58CC02',
          light: '#89E219',
          dark: '#4CAF00',
        },
        secondary: {
          DEFAULT: '#1CB0F6',
          light: '#4FC3F7',
          dark: '#0091EA',
        },
        accent: {
          orange: '#FF9600',
          red: '#FF4B4B',
          purple: '#CE82FF',
        },
        neutral: {
          bg: '#F7F7F7',
          card: '#FFFFFF',
          text: '#3C3C3C',
          muted: '#AFAFAF',
        },
      },
      fontFamily: {
        sans: ['Pretendard', '-apple-system', 'BlinkMacSystemFont', 'system-ui', 'sans-serif'],
      },
      animation: {
        'bounce-subtle': 'bounce-subtle 0.3s ease-out',
        'shake': 'shake 0.5s ease-in-out',
        'confetti': 'confetti 1s ease-out',
      },
      keyframes: {
        'bounce-subtle': {
          '0%, 100%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.05)' },
        },
        'shake': {
          '0%, 100%': { transform: 'translateX(0)' },
          '25%': { transform: 'translateX(-5px)' },
          '75%': { transform: 'translateX(5px)' },
        },
        'confetti': {
          '0%': { opacity: '1', transform: 'translateY(0)' },
          '100%': { opacity: '0', transform: 'translateY(-100px)' },
        },
      },
    },
  },
  plugins: [],
}

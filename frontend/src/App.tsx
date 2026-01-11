import { Routes, Route } from 'react-router-dom'

function App() {
  return (
    <div className="min-h-screen bg-neutral-bg">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/quiz" element={<Quiz />} />
        <Route path="/result" element={<Result />} />
      </Routes>
    </div>
  )
}

// 임시 페이지 컴포넌트 (추후 pages/로 분리)
function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <h1 className="text-4xl font-bold text-neutral-text mb-4">
        의원얼굴퀴즈
      </h1>
      <p className="text-lg text-neutral-muted mb-8">
        경기도의회 11대 의원 얼굴 맞추기
      </p>
      <a
        href="/quiz"
        className="px-8 py-4 bg-primary text-white font-bold rounded-2xl
                   hover:bg-primary-dark transition-colors
                   shadow-lg hover:shadow-xl"
      >
        퀴즈 시작하기
      </a>
    </div>
  )
}

function Quiz() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <p className="text-lg text-neutral-muted">퀴즈 페이지 (개발 예정)</p>
    </div>
  )
}

function Result() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <p className="text-lg text-neutral-muted">결과 페이지 (개발 예정)</p>
    </div>
  )
}

export default App

/**
 * 의원얼굴퀴즈 앱
 */
import { Routes, Route } from 'react-router-dom';
import { MainPage, QuizPage, ResultPage } from './pages';

function App() {
  return (
    <div className="min-h-screen bg-neutral-bg">
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/quiz" element={<QuizPage />} />
        <Route path="/result" element={<ResultPage />} />
      </Routes>
    </div>
  );
}

export default App;

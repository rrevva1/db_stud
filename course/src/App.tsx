import { Routes, Route, Navigate } from "react-router-dom";
import { useCourseData } from "./hooks/useCourseData";
import { useProgress } from "./hooks/useProgress";
import HomePage from "./pages/HomePage";
import LessonPage from "./pages/LessonPage";
import Layout from "./components/Layout";

export default function App() {
  const { curriculum, sources, error, loading } = useCourseData();
  const progressApi = useProgress();

  if (loading) {
    return (
      <div className="loading-screen">
        <p>Загрузка курса…</p>
      </div>
    );
  }

  if (error || !curriculum || !sources) {
    return (
      <div className="loading-screen error">
        <h1>Ошибка загрузки</h1>
        <p>{error ?? "Не удалось загрузить данные курса."}</p>
        <p className="hint">
          Запустите локальный сервер из папки <code>course</code>:{" "}
          <code>npm run dev</code> или <code>python -m http.server 8080</code>
        </p>
      </div>
    );
  }

  return (
    <Layout curriculum={curriculum} progressApi={progressApi}>
      <Routes>
        <Route
          path="/"
          element={
            <HomePage curriculum={curriculum} progressApi={progressApi} />
          }
        />
        <Route
          path="/lesson/:lessonId"
          element={
            <LessonPage
              curriculum={curriculum}
              sources={sources}
              progressApi={progressApi}
            />
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  );
}

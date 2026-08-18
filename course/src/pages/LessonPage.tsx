import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { marked } from "marked";
import type { Curriculum, Quiz, SourcesCatalog } from "../types";
import { findLesson, nextLessonId } from "../types";
import type { useProgress } from "../hooks/useProgress";
import {
  loadLessonMarkdown,
  loadLessonQuiz,
  loadLessonTasks,
} from "../hooks/useCourseData";
import SourceLinks from "../components/SourceLinks";
import QuizBlock from "../components/Quiz";
import TasksBlock from "../components/Tasks";

type ProgressApi = ReturnType<typeof useProgress>;

interface LessonPageProps {
  curriculum: Curriculum;
  sources: SourcesCatalog;
  progressApi: ProgressApi;
}

export default function LessonPage({
  curriculum,
  sources,
  progressApi,
}: LessonPageProps) {
  const { lessonId } = useParams<{ lessonId: string }>();
  const [theory, setTheory] = useState("");
  const [tasks, setTasks] = useState("");
  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [loading, setLoading] = useState(true);

  const found = lessonId ? findLesson(curriculum, lessonId) : null;
  const nextId = lessonId ? nextLessonId(curriculum, lessonId) : null;

  useEffect(() => {
    if (!lessonId) return;
    setLoading(true);
    Promise.all([
      loadLessonMarkdown(lessonId),
      loadLessonTasks(lessonId),
      loadLessonQuiz(lessonId),
    ]).then(([md, t, q]) => {
      setTheory(md);
      setTasks(t);
      setQuiz(q);
      setLoading(false);
    });
  }, [lessonId]);

  if (!lessonId || !found) {
    return (
      <div className="lesson-error">
        <p>Урок не найден.</p>
        <Link to="/">На главную</Link>
      </div>
    );
  }

  const { lesson, part, module: mod } = found;
  const theoryHtml = marked.parse(theory) as string;

  return (
    <article className="lesson">
      <nav className="breadcrumb">
        <Link to="/">Курс</Link>
        <span> / </span>
        <span>{part.title}</span>
        <span> / </span>
        <span>{mod.title}</span>
      </nav>

      <header className="lesson-header">
        <h1>{lesson.title}</h1>
        <div className="lesson-meta">
          <span className={`dialect dialect-${lesson.dialect}`}>
            {lesson.dialect}
          </span>
          {progressApi.isCompleted(lessonId) && (
            <span className="completed-badge">Пройден</span>
          )}
        </div>
        {lesson.objectives.length > 0 && (
          <ul className="objectives">
            {lesson.objectives.map((o, i) => (
              <li key={i}>{o}</li>
            ))}
          </ul>
        )}
      </header>

      {loading ? (
        <p>Загрузка урока…</p>
      ) : (
        <>
          <section className="theory-block">
            <h2>Теория</h2>
            <div
              className="markdown"
              dangerouslySetInnerHTML={{ __html: theoryHtml }}
            />
          </section>

          <SourceLinks
            required={lesson.requiredSources}
            optional={lesson.optionalSources}
            sources={sources}
          />

          {quiz && (
            <QuizBlock
              quiz={quiz}
              onPass={(score) => {
                progressApi.setQuizScore(lessonId, score);
              }}
            />
          )}

          <TasksBlock markdown={tasks} />

          <footer className="lesson-footer">
            <button
              type="button"
              className="btn-primary"
              onClick={() => progressApi.markCompleted(lessonId)}
              disabled={progressApi.isCompleted(lessonId)}
            >
              {progressApi.isCompleted(lessonId)
                ? "Урок отмечен пройденным"
                : "Отметить урок пройденным"}
            </button>
            {nextId && (
              <Link to={`/lesson/${nextId}`} className="btn-secondary">
                Следующий урок →
              </Link>
            )}
          </footer>
        </>
      )}
    </article>
  );
}

import { Link } from "react-router-dom";
import type { Curriculum } from "../types";
import type { useProgress } from "../hooks/useProgress";
import { flattenLessons } from "../types";

type ProgressApi = ReturnType<typeof useProgress>;

interface HomePageProps {
  curriculum: Curriculum;
  progressApi: ProgressApi;
}

export default function HomePage({ curriculum, progressApi }: HomePageProps) {
  const total = flattenLessons(curriculum).length;
  const done = progressApi.totalCompleted;
  const pct = total ? Math.round((done / total) * 100) : 0;

  return (
    <div className="home">
      <h1>{curriculum.title}</h1>
      <p className="subtitle">
        Курс в формате Stepik: теория → источники (PDF) → тест → практика.
        Практика SQL выполняется в PostgreSQL.
      </p>

      <div className="stats-grid">
        <div className="stat-card">
          <span className="stat-value">{curriculum.parts.length}</span>
          <span className="stat-label">частей</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{total}</span>
          <span className="stat-label">уроков</span>
        </div>
        <div className="stat-card accent">
          <span className="stat-value">{pct}%</span>
          <span className="stat-label">прогресс</span>
        </div>
      </div>

      <section className="home-parts">
        <h2>Программа курса</h2>
        {curriculum.parts.map((part) => {
          const partLessons = part.modules.flatMap((m) => m.lessons);
          const partDone = partLessons.filter((l) =>
            progressApi.isCompleted(l.id)
          ).length;
          return (
            <details key={part.id} className="part-card" open={part.id === "part0"}>
              <summary>
                <strong>{part.title}</strong>
                <span className="part-progress">
                  {partDone}/{partLessons.length}
                </span>
              </summary>
              <ul>
                {part.modules.map((mod) => (
                  <li key={mod.id}>
                    <span className="mod-name">{mod.title}</span>
                    <ul>
                      {mod.lessons.map((l) => (
                        <li key={l.id}>
                          <Link to={`/lesson/${l.id}`}>{l.title}</Link>
                          {progressApi.isCompleted(l.id) && " ✓"}
                        </li>
                      ))}
                    </ul>
                  </li>
                ))}
              </ul>
            </details>
          );
        })}
      </section>

      <section className="home-how">
        <h2>Как учиться</h2>
        <ol>
          <li>Прочитайте теорию урока (краткий пересказ).</li>
          <li>
            Откройте указанные главы PDF из папки <code>db_stud</code>.
          </li>
          <li>Пройдите тест (обычно порог 70%).</li>
          <li>
            Выполните практику в PostgreSQL; сверьтесь с эталоном в{" "}
            <code>course/sql/</code>.
          </li>
        </ol>
      </section>
    </div>
  );
}

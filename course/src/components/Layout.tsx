import { Link } from "react-router-dom";
import type { ReactNode } from "react";
import type { Curriculum } from "../types";
import type { useProgress } from "../hooks/useProgress";
import Sidebar from "./Sidebar";

type ProgressApi = ReturnType<typeof useProgress>;

interface LayoutProps {
  children: ReactNode;
  curriculum: Curriculum;
  progressApi: ProgressApi;
}

export default function Layout({
  children,
  curriculum,
  progressApi,
}: LayoutProps) {
  return (
    <div className="layout">
      <header className="header">
        <Link to="/" className="logo">
          {curriculum.title}
        </Link>
        <div className="header-meta">
          <span className="progress-badge">
            Пройдено: {progressApi.totalCompleted} /{" "}
            {curriculum.parts.reduce(
              (n, p) =>
                n + p.modules.reduce((m, mod) => m + mod.lessons.length, 0),
              0
            )}
          </span>
          <button
            type="button"
            className="btn-ghost"
            onClick={() => {
              if (confirm("Сбросить весь прогресс?")) {
                progressApi.resetProgress();
              }
            }}
          >
            Сброс
          </button>
        </div>
      </header>
      <div className="body">
        <Sidebar curriculum={curriculum} progressApi={progressApi} />
        <main className="main">{children}</main>
      </div>
    </div>
  );
}

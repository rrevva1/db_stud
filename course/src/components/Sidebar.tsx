import { Link, useParams } from "react-router-dom";
import type { Curriculum } from "../types";
import type { useProgress } from "../hooks/useProgress";

type ProgressApi = ReturnType<typeof useProgress>;

interface SidebarProps {
  curriculum: Curriculum;
  progressApi: ProgressApi;
  collapsed?: boolean;
}

export default function Sidebar({
  curriculum,
  progressApi,
  collapsed,
}: SidebarProps) {
  const { lessonId } = useParams();

  return (
    <aside className={`sidebar ${collapsed ? "sidebar-collapsed" : ""}`}>
      <nav className="sidebar-nav">
        {curriculum.parts.map((part) => (
          <div key={part.id} className="sidebar-part">
            <h3 className="sidebar-part-title">{part.title}</h3>
            {part.modules.map((mod) => (
              <div key={mod.id} className="sidebar-module">
                <h4 className="sidebar-module-title">{mod.title}</h4>
                <ul className="sidebar-lessons">
                  {mod.lessons.map((lesson) => {
                    const done = progressApi.isCompleted(lesson.id);
                    const active = lessonId === lesson.id;
                    return (
                      <li key={lesson.id}>
                        <Link
                          to={`/lesson/${lesson.id}`}
                          className={`sidebar-link ${active ? "active" : ""} ${done ? "done" : ""}`}
                        >
                          <span className="lesson-status">
                            {done ? "✓" : "○"}
                          </span>
                          {lesson.title}
                        </Link>
                      </li>
                    );
                  })}
                </ul>
              </div>
            ))}
          </div>
        ))}
      </nav>
    </aside>
  );
}

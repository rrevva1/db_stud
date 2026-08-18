import { useEffect, useState } from "react";
import type { Curriculum, SourcesCatalog } from "../types";

export function useCourseData() {
  const [curriculum, setCurriculum] = useState<Curriculum | null>(null);
  const [sources, setSources] = useState<SourcesCatalog | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      fetch(`${import.meta.env.BASE_URL}content/curriculum.json`).then((r) => {
        if (!r.ok) throw new Error("curriculum.json");
        return r.json();
      }),
      fetch(`${import.meta.env.BASE_URL}content/sources.json`).then((r) => {
        if (!r.ok) throw new Error("sources.json");
        return r.json();
      }),
    ])
      .then(([c, s]) => {
        setCurriculum(c);
        setSources(s);
      })
      .catch((e) => setError(String(e)));
  }, []);

  return { curriculum, sources, error, loading: !curriculum && !error };
}

export async function loadLessonMarkdown(lessonId: string): Promise<string> {
  const res = await fetch(
    `${import.meta.env.BASE_URL}content/lessons/${lessonId}.md`
  );
  if (!res.ok) return "*Текст урока не найден.*";
  return res.text();
}

export async function loadLessonTasks(lessonId: string): Promise<string> {
  const res = await fetch(
    `${import.meta.env.BASE_URL}content/lessons/${lessonId}.tasks.md`
  );
  if (!res.ok) return "";
  return res.text();
}

export async function loadLessonQuiz(lessonId: string) {
  const res = await fetch(
    `${import.meta.env.BASE_URL}content/lessons/${lessonId}.quiz.json`
  );
  if (!res.ok) return null;
  return res.json();
}

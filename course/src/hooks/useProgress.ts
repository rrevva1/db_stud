import { useCallback, useEffect, useState } from "react";
import type { ProgressState } from "../types";

const STORAGE_KEY = "db-stud-course-progress-v1";

const defaultState: ProgressState = {
  completedLessons: [],
  quizScores: {},
};

function load(): ProgressState {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { ...defaultState };
    return { ...defaultState, ...JSON.parse(raw) };
  } catch {
    return { ...defaultState };
  }
}

function save(state: ProgressState) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

export function useProgress() {
  const [progress, setProgress] = useState<ProgressState>(load);

  useEffect(() => {
    save(progress);
  }, [progress]);

  const markCompleted = useCallback((lessonId: string) => {
    setProgress((p) => {
      if (p.completedLessons.includes(lessonId)) return p;
      return {
        ...p,
        completedLessons: [...p.completedLessons, lessonId],
      };
    });
  }, []);

  const setQuizScore = useCallback((lessonId: string, score: number) => {
    setProgress((p) => ({
      ...p,
      quizScores: { ...p.quizScores, [lessonId]: score },
    }));
  }, []);

  const resetProgress = useCallback(() => {
    setProgress({ ...defaultState });
  }, []);

  const isCompleted = useCallback(
    (lessonId: string) => progress.completedLessons.includes(lessonId),
    [progress.completedLessons]
  );

  const totalCompleted = progress.completedLessons.length;

  return {
    progress,
    markCompleted,
    setQuizScore,
    resetProgress,
    isCompleted,
    totalCompleted,
  };
}

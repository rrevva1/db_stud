export interface SourceRef {
  sourceId: string;
  ref: string;
}

export interface LessonMeta {
  id: string;
  title: string;
  dialect: string;
  requiredSources: SourceRef[];
  optionalSources: SourceRef[];
  objectives: string[];
}

export interface Module {
  id: string;
  title: string;
  lessons: LessonMeta[];
}

export interface Part {
  id: string;
  title: string;
  modules: Module[];
}

export interface Curriculum {
  title: string;
  version: string;
  parts: Part[];
}

export interface Source {
  id: string;
  title: string;
  authors: string;
  path: string;
  language: string;
  role: string;
}

export interface SourcesCatalog {
  sources: Source[];
}

export interface QuizQuestion {
  id: string;
  type: "single" | "multi";
  question: string;
  options: string[];
  correct: number[];
  explanation: string;
}

export interface Quiz {
  lessonId: string;
  passingScore: number;
  questions: QuizQuestion[];
}

export interface ProgressState {
  completedLessons: string[];
  quizScores: Record<string, number>;
}

export function flattenLessons(curriculum: Curriculum): LessonMeta[] {
  const out: LessonMeta[] = [];
  for (const part of curriculum.parts) {
    for (const mod of part.modules) {
      out.push(...mod.lessons);
    }
  }
  return out;
}

export function findLesson(
  curriculum: Curriculum,
  lessonId: string
): { lesson: LessonMeta; part: Part; module: Module } | null {
  for (const part of curriculum.parts) {
    for (const mod of part.modules) {
      const lesson = mod.lessons.find((l) => l.id === lessonId);
      if (lesson) return { lesson, part, module: mod };
    }
  }
  return null;
}

export function nextLessonId(
  curriculum: Curriculum,
  currentId: string
): string | null {
  const flat = flattenLessons(curriculum);
  const idx = flat.findIndex((l) => l.id === currentId);
  if (idx < 0 || idx >= flat.length - 1) return null;
  return flat[idx + 1].id;
}

import { useMemo, useState } from "react";
import type { Quiz, QuizQuestion } from "../types";

interface QuizProps {
  quiz: Quiz;
  onPass: (score: number) => void;
}

function shuffleIndices(n: number): number[] {
  const idx = Array.from({ length: n }, (_, i) => i);
  for (let i = n - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [idx[i], idx[j]] = [idx[j], idx[i]];
  }
  return idx;
}

function shuffleQuestion(q: QuizQuestion): QuizQuestion {
  const order = shuffleIndices(q.options.length);
  return {
    ...q,
    options: order.map((i) => q.options[i]),
    correct: q.correct.map((c) => order.indexOf(c)).sort((a, b) => a - b),
  };
}

export default function QuizBlock({ quiz, onPass }: QuizProps) {
  const [shuffleKey, setShuffleKey] = useState(0);
  const questions = useMemo(
    () => quiz.questions.map(shuffleQuestion),
    [quiz, shuffleKey]
  );
  const [answers, setAnswers] = useState<Record<string, number[]>>({});
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(0);

  const toggle = (qId: string, idx: number, multi: boolean) => {
    if (submitted) return;
    setAnswers((prev) => {
      const cur = prev[qId] ?? [];
      if (multi) {
        const next = cur.includes(idx)
          ? cur.filter((i) => i !== idx)
          : [...cur, idx];
        return { ...prev, [qId]: next.sort() };
      }
      return { ...prev, [qId]: [idx] };
    });
  };

  const submit = () => {
    let correct = 0;
    for (const q of questions) {
      const user = [...(answers[q.id] ?? [])].sort();
      const expected = [...q.correct].sort();
      if (
        user.length === expected.length &&
        user.every((v, i) => v === expected[i])
      ) {
        correct++;
      }
    }
    const pct = Math.round((correct / questions.length) * 100);
    setScore(pct);
    setSubmitted(true);
    if (pct >= quiz.passingScore) onPass(pct);
  };

  const retry = () => {
    setSubmitted(false);
    setAnswers({});
    setScore(0);
    setShuffleKey((k) => k + 1);
  };

  return (
    <section className="quiz-block">
      <h2>Тест</h2>
      {!submitted && (
        <p className="quiz-hint">
          Для прохождения нужно набрать не менее {quiz.passingScore}%.
        </p>
      )}
      {questions.map((q, qi) => (
        <div key={`${shuffleKey}-${q.id}`} className="quiz-question">
          <p className="question-text">
            {qi + 1}. {q.question}
            {q.type === "multi" && (
              <span className="multi-hint"> (несколько ответов)</span>
            )}
          </p>
          <ul className="quiz-options">
            {q.options.map((opt, oi) => {
              const selected = (answers[q.id] ?? []).includes(oi);
              const isCorrect = q.correct.includes(oi);
              let cls = "quiz-option";
              if (submitted) {
                if (isCorrect) cls += " correct";
                else if (selected) cls += " wrong";
              } else if (selected) cls += " selected";
              return (
                <li key={oi}>
                  <button
                    type="button"
                    className={cls}
                    onClick={() => toggle(q.id, oi, q.type === "multi")}
                  >
                    {opt}
                  </button>
                </li>
              );
            })}
          </ul>
          {submitted && <p className="explanation">{q.explanation}</p>}
        </div>
      ))}
      {!submitted ? (
        <button type="button" className="btn-primary" onClick={submit}>
          Проверить ответы
        </button>
      ) : (
        <div
          className={`quiz-result ${score >= quiz.passingScore ? "pass" : "fail"}`}
        >
          Результат: {score}%{" "}
          {score >= quiz.passingScore ? "— тест пройден" : "— попробуйте ещё раз"}
          {score < quiz.passingScore && (
            <button type="button" className="btn-ghost retry" onClick={retry}>
              Пройти заново
            </button>
          )}
        </div>
      )}
    </section>
  );
}

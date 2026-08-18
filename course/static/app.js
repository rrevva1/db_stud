const STORAGE_KEY = "db-stud-course-progress-v1";
const CONTENT_BASE = new URL("../public/content/", import.meta.url).href;

let curriculum = null;
let sources = null;
let progress = loadProgress();

function loadProgress() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { completedLessons: [], quizScores: {} };
    return { completedLessons: [], quizScores: {}, ...JSON.parse(raw) };
  } catch {
    return { completedLessons: [], quizScores: {} };
  }
}

function saveProgress() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
}

function flattenLessons(c) {
  const out = [];
  for (const part of c.parts) {
    for (const mod of part.modules) {
      out.push(...mod.lessons);
    }
  }
  return out;
}

function findLesson(lessonId) {
  for (const part of curriculum.parts) {
    for (const mod of part.modules) {
      const lesson = mod.lessons.find((l) => l.id === lessonId);
      if (lesson) return { lesson, part, mod };
    }
  }
  return null;
}

function nextLessonId(currentId) {
  const flat = flattenLessons(curriculum);
  const idx = flat.findIndex((l) => l.id === currentId);
  if (idx < 0 || idx >= flat.length - 1) return null;
  return flat[idx + 1].id;
}

function isCompleted(id) {
  return progress.completedLessons.includes(id);
}

function totalLessons() {
  return flattenLessons(curriculum).length;
}

function escapeHtml(s) {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function renderSidebar(activeId) {
  let html = '<aside class="sidebar"><nav class="sidebar-nav">';
  for (const part of curriculum.parts) {
    html += `<h3 class="sidebar-part-title">${escapeHtml(part.title)}</h3>`;
    for (const mod of part.modules) {
      html += `<h4 class="sidebar-module-title">${escapeHtml(mod.title)}</h4>`;
      html += '<ul class="sidebar-lessons">';
      for (const lesson of mod.lessons) {
        const done = isCompleted(lesson.id);
        const active = lesson.id === activeId;
        html += `<li><a href="#/lesson/${lesson.id}" class="sidebar-link${active ? " active" : ""}${done ? " done" : ""}">`;
        html += `<span class="lesson-status">${done ? "✓" : "○"}</span>`;
        html += escapeHtml(lesson.title);
        html += "</a></li>";
      }
      html += "</ul>";
    }
  }
  html += "</nav></aside>";
  return html;
}

function renderHeader() {
  return `
    <header class="header">
      <a href="#/" class="logo">${escapeHtml(curriculum.title)}</a>
      <div class="header-meta">
        <span class="progress-badge">Пройдено: ${progress.completedLessons.length} / ${totalLessons()}</span>
        <button type="button" class="btn-ghost" id="reset-progress">Сброс</button>
      </div>
    </header>`;
}

function renderHome() {
  const total = totalLessons();
  const done = progress.completedLessons.length;
  const pct = total ? Math.round((done / total) * 100) : 0;

  let partsHtml = "";
  for (const part of curriculum.parts) {
    const partLessons = part.modules.flatMap((m) => m.lessons);
    const partDone = partLessons.filter((l) => isCompleted(l.id)).length;
    partsHtml += `<details class="part-card"${part.id === "part0" ? " open" : ""}>`;
    partsHtml += `<summary><strong>${escapeHtml(part.title)}</strong>`;
    partsHtml += `<span class="part-progress">${partDone}/${partLessons.length}</span></summary><ul>`;
    for (const mod of part.modules) {
      partsHtml += `<li><span class="mod-name">${escapeHtml(mod.title)}</span><ul>`;
      for (const l of mod.lessons) {
        const mark = isCompleted(l.id) ? " ✓" : "";
        partsHtml += `<li><a href="#/lesson/${l.id}">${escapeHtml(l.title)}</a>${mark}</li>`;
      }
      partsHtml += "</ul></li>";
    }
    partsHtml += "</ul></details>";
  }

  return `
    <div class="home">
      <h1>${escapeHtml(curriculum.title)}</h1>
      <p class="subtitle">Курс в формате Stepik: теория → источники (PDF) → тест → практика. Практика SQL — PostgreSQL.</p>
      <div class="stats-grid">
        <div class="stat-card"><span class="stat-value">${curriculum.parts.length}</span><span class="stat-label">частей</span></div>
        <div class="stat-card"><span class="stat-value">${total}</span><span class="stat-label">уроков</span></div>
        <div class="stat-card accent"><span class="stat-value">${pct}%</span><span class="stat-label">прогресс</span></div>
      </div>
      <section class="home-parts"><h2>Программа курса</h2>${partsHtml}</section>
      <section class="home-how">
        <h2>Как учиться</h2>
        <ol>
          <li>Прочитайте теорию урока.</li>
          <li>Откройте главы PDF из папки <code>db_stud</code>.</li>
          <li>Пройдите тест (порог 70%).</li>
          <li>Выполните практику в PostgreSQL; эталоны — в <code>course/sql/</code>.</li>
        </ol>
      </section>
    </div>`;
}

function sourceHeading(src, fallbackId) {
  if (!src) return fallbackId;
  return src.authors ? `${src.authors} — ${src.title}` : src.title;
}

function renderSources(lesson) {
  const resolve = (ref) => sources.sources.find((s) => s.id === ref.sourceId);
  let html = `<section class="sources-block"><h2>Источники для изучения</h2>`;
  html += `<p class="sources-note">Читайте в указанной очереди. Текст книг в урок не включён — оригиналы в папке <code>sources/</code>.</p>`;
  if (lesson.requiredSources?.length) {
    html += "<h3>Очередь чтения</h3><ol class=\"sources-list sources-queue\">";
    lesson.requiredSources.forEach((r, i) => {
      const src = resolve(r);
      html += "<li>";
      html += `<span class="queue-label">${i + 1}-я очередь</span>`;
      html += `<strong>${escapeHtml(sourceHeading(src, r.sourceId))}</strong>`;
      html += `<br><span class="ref">${escapeHtml(r.ref)}</span>`;
      if (src?.path) html += `<br><code class="path">${escapeHtml(src.path)}</code>`;
      html += "</li>";
    });
    html += "</ol>";
  }
  if (lesson.optionalSources?.length) {
    html += "<h3>Далее (по желанию)</h3><ul class=\"sources-list optional\">";
    for (const r of lesson.optionalSources) {
      const src = resolve(r);
      html += "<li>";
      html += `<strong>${escapeHtml(sourceHeading(src, r.sourceId))}</strong>`;
      html += `<br><span class="ref">${escapeHtml(r.ref)}</span>`;
      html += "</li>";
    }
    html += "</ul>";
  }
  html += "</section>";
  return html;
}

function shuffleQuestion(q) {
  const n = q.options.length;
  const order = Array.from({ length: n }, (_, i) => i);
  for (let i = n - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [order[i], order[j]] = [order[j], order[i]];
  }
  return {
    ...q,
    options: order.map((i) => q.options[i]),
    correct: q.correct.map((c) => order.indexOf(c)).sort((a, b) => a - b),
  };
}

function renderQuiz(quiz, lessonId) {
  if (!quiz?.questions?.length) return "";
  const qJson = escapeHtml(JSON.stringify(quiz));
  return `<section class="quiz-block" data-quiz="${qJson}" data-lesson="${lessonId}">
    <h2>Тест</h2>
    <p class="quiz-hint">Для прохождения нужно набрать не менее ${quiz.passingScore}%.</p>
    <div class="quiz-body"></div>
  </section>`;
}

function mountQuiz(container) {
  const section = container.querySelector(".quiz-block");
  if (!section) return;
  const original = JSON.parse(section.dataset.quiz);
  const lessonId = section.dataset.lesson;
  const body = section.querySelector(".quiz-body");
  const answers = {};
  let quiz = {
    ...original,
    questions: original.questions.map(shuffleQuestion),
  };

  function reshuffle() {
    quiz = {
      ...original,
      questions: original.questions.map(shuffleQuestion),
    };
  }

  function renderQuestions(submitted, score) {
    let html = "";
    quiz.questions.forEach((q, qi) => {
      html += `<div class="quiz-question" data-qid="${q.id}">`;
      html += `<p class="question-text">${qi + 1}. ${escapeHtml(q.question)}`;
      if (q.type === "multi") html += '<span class="multi-hint"> (несколько ответов)</span>';
      html += "</p><ul class=\"quiz-options\">";
      q.options.forEach((opt, oi) => {
        const selected = (answers[q.id] ?? []).includes(oi);
        const isCorrect = q.correct.includes(oi);
        let cls = "quiz-option";
        if (submitted) {
          if (isCorrect) cls += " correct";
          else if (selected) cls += " wrong";
        } else if (selected) cls += " selected";
        html += `<li><button type="button" class="${cls}" data-q="${q.id}" data-oi="${oi}" data-multi="${q.type === "multi"}">${escapeHtml(opt)}</button></li>`;
      });
      html += "</ul>";
      if (submitted) html += `<p class="explanation">${escapeHtml(q.explanation)}</p>`;
      html += "</div>";
    });

    if (!submitted) {
      html += '<button type="button" class="btn-primary" id="quiz-submit">Проверить ответы</button>';
    } else {
      const pass = score >= quiz.passingScore;
      html += `<div class="quiz-result ${pass ? "pass" : "fail"}">Результат: ${score}% — ${pass ? "тест пройден" : "попробуйте ещё раз"}`;
      if (!pass) html += ' <button type="button" class="btn-ghost retry" id="quiz-retry">Пройти заново</button>';
      html += "</div>";
    }
    body.innerHTML = html;

    if (!submitted) {
      body.querySelectorAll(".quiz-option").forEach((btn) => {
        btn.addEventListener("click", () => {
          const qid = btn.dataset.q;
          const oi = Number(btn.dataset.oi);
          const multi = btn.dataset.multi === "true";
          const cur = answers[qid] ?? [];
          if (multi) {
            answers[qid] = cur.includes(oi) ? cur.filter((i) => i !== oi) : [...cur, oi].sort();
          } else {
            answers[qid] = [oi];
          }
          renderQuestions(false, 0);
        });
      });
      body.querySelector("#quiz-submit")?.addEventListener("click", () => {
        let correct = 0;
        for (const q of quiz.questions) {
          const user = [...(answers[q.id] ?? [])].sort();
          const expected = [...q.correct].sort();
          if (user.length === expected.length && user.every((v, i) => v === expected[i])) correct++;
        }
        const pct = Math.round((correct / quiz.questions.length) * 100);
        if (pct >= quiz.passingScore) {
          progress.quizScores[lessonId] = pct;
          saveProgress();
        }
        renderQuestions(true, pct);
      });
    } else {
      body.querySelector("#quiz-retry")?.addEventListener("click", () => {
        Object.keys(answers).forEach((k) => delete answers[k]);
        reshuffle();
        renderQuestions(false, 0);
      });
    }
  }

  renderQuestions(false, 0);
}

async function renderLesson(lessonId) {
  const found = findLesson(lessonId);
  if (!found) {
    return `<div class="lesson-error"><p>Урок не найден.</p><a href="#/">На главную</a></div>`;
  }

  const { lesson, part, mod } = found;
  const [mdRes, tasksRes, quizRes] = await Promise.all([
    fetch(`${CONTENT_BASE}lessons/${lessonId}.md`),
    fetch(`${CONTENT_BASE}lessons/${lessonId}.tasks.md`),
    fetch(`${CONTENT_BASE}lessons/${lessonId}.quiz.json`),
  ]);

  const theory = mdRes.ok ? await mdRes.text() : "*Текст урока не найден.*";
  const tasks = tasksRes.ok ? await tasksRes.text() : "";
  const quiz = quizRes.ok ? await quizRes.json() : null;
  const theoryHtml = marked.parse(theory);
  const tasksHtml = tasks ? marked.parse(tasks) : "";
  const done = isCompleted(lessonId);
  const nextId = nextLessonId(lessonId);

  let objectives = "";
  if (lesson.objectives?.length) {
    objectives = "<ul class=\"objectives\">" + lesson.objectives.map((o) => `<li>${escapeHtml(o)}</li>`).join("") + "</ul>";
  }

  return `
    <article class="lesson">
      <nav class="breadcrumb"><a href="#/">Курс</a> / ${escapeHtml(part.title)} / ${escapeHtml(mod.title)}</nav>
      <header class="lesson-header">
        <h1>${escapeHtml(lesson.title)}</h1>
        <div class="lesson-meta">
          <span class="dialect">${escapeHtml(lesson.dialect)}</span>
          ${done ? '<span class="completed-badge">Пройден</span>' : ""}
        </div>
        ${objectives}
      </header>
      <section class="theory-block"><h2>Теория</h2><div class="markdown">${theoryHtml}</div></section>
      ${renderSources(lesson)}
      ${renderQuiz(quiz, lessonId)}
      ${tasksHtml ? `<section class="tasks-block"><h2>Практика</h2><div class="markdown">${tasksHtml}</div></section>` : ""}
      <footer class="lesson-footer">
        <button type="button" class="btn-primary" id="mark-done"${done ? " disabled" : ""}>${done ? "Урок отмечен пройденным" : "Отметить урок пройденным"}</button>
        ${nextId ? `<a href="#/lesson/${nextId}" class="btn-secondary">Следующий урок →</a>` : ""}
      </footer>
    </article>`;
}

function layout(content, activeId) {
  return `
    <div class="layout">
      ${renderHeader()}
      <div class="body">
        ${renderSidebar(activeId)}
        <main class="main">${content}</main>
      </div>
    </div>`;
}

function bindGlobalHandlers() {
  document.getElementById("reset-progress")?.addEventListener("click", () => {
    if (confirm("Сбросить весь прогресс?")) {
      progress = { completedLessons: [], quizScores: {} };
      saveProgress();
      route();
    }
  });
}

async function route() {
  const hash = location.hash.slice(1) || "/";
  const app = document.getElementById("app");

  if (hash === "/" || hash === "") {
    app.innerHTML = layout(renderHome(), null);
    bindGlobalHandlers();
    return;
  }

  const match = hash.match(/^\/lesson\/([^/]+)$/);
  if (match) {
    const lessonId = match[1];
    app.innerHTML = layout('<p>Загрузка урока…</p>', lessonId);
    bindGlobalHandlers();
    const html = await renderLesson(lessonId);
    app.innerHTML = layout(html, lessonId);
    bindGlobalHandlers();
    mountQuiz(app);

    document.getElementById("mark-done")?.addEventListener("click", () => {
      if (!progress.completedLessons.includes(lessonId)) {
        progress.completedLessons.push(lessonId);
        saveProgress();
        route();
      }
    });
    return;
  }

  app.innerHTML = layout("<p>Страница не найдена.</p>", null);
  bindGlobalHandlers();
}

async function init() {
  const app = document.getElementById("app");
  try {
    const [cRes, sRes] = await Promise.all([
      fetch(`${CONTENT_BASE}curriculum.json`),
      fetch(`${CONTENT_BASE}sources.json`),
    ]);
    if (!cRes.ok || !sRes.ok) throw new Error("Не удалось загрузить curriculum.json или sources.json");
    curriculum = await cRes.json();
    sources = await sRes.json();
    window.addEventListener("hashchange", route);
    await route();
  } catch (e) {
    app.innerHTML = `
      <div class="loading-screen error">
        <h1>Ошибка загрузки</h1>
        <p>${escapeHtml(String(e))}</p>
        <p class="hint">Запустите из папки <code>course</code>:<br>
        <code>python -m http.server 8080</code><br>
        Откройте <code>http://localhost:8080/static/</code></p>
      </div>`;
  }
}

init();

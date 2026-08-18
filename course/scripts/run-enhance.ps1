# Build JSON data files from Python lesson definitions and write all lesson files
$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $scriptDir
$node = "c:\Users\RevvaRR\AppData\Local\Programs\cursor\resources\app\resources\helpers\node.exe"

# Convert Python lesson scripts to JSON via Node helper
$converter = @'
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { createRequire } from "module";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function sq(qid, question, options, correct, explanation) {
  return { id: qid, type: "single", question, options, correct: [correct], explanation };
}
function mq(qid, question, options, correct, explanation) {
  return { id: qid, type: "multi", question, options, correct, explanation };
}
function quiz(lessonId, ...questions) {
  return { lessonId, passingScore: 70, questions };
}
function md(title, part, mod, dialectNote, objectives, theory, sources, concepts, extra = "") {
  const obj = objectives.map(o => `- ${o}`).join("\n");
  const src = sources.map(s => `- **${s[0]}**: ${s[1]}`).join("\n");
  const con = concepts.map(c => `- **${c[0]}** — ${c[1]}.`).join("\n");
  return `## ${title}

**Часть:** ${part} · **Модуль:** ${mod}

${dialectNote}

### Цели урока

${obj}

### Краткая теория

${theory}

### Что читать в источниках

${src}

### Ключевые понятия

${con}
${extra}`;
}

const P6 = "Внутреннее устройство PostgreSQL";
const M6 = "Хранение и расширения";
const P7 = "Администрирование и архитектуры нагрузок";
const M7 = "Безопасность и эксплуатация";
const P8 = "Хранилища данных";
const M8 = "DWH и dimensional modeling";
const P9 = "Альтернативные СУБД и итоговая аттестация";
const M9A = "NoSQL и графовые БД";
const M9B = "T-SQL, теория Дейта и итог";
const SQL = "Практика: **PostgreSQL** (psql или pgAdmin).";
const TH = "Фокус на теории и тесте; SQL не обязателен.";
const LAB = "Лaboratornaya. Sreda: **PostgreSQL**.";
const EX = "Итоговый тест части.";
const CMP = "> **Сравнение диалектов:** T-SQL (SQL Server) ↔ PostgreSQL\n";
const OPT = "> **Опционально:** задания можно выполнить на [MongoDB Playground](https://mongoplayground.net) без локальной установки.\n";

const LESSONS = {};
'@

# Read part2 python and extract LESSONS assignments - use node dynamic import of compiled bundle
# Instead: run full bundled mjs
'@

Write-Host "Use bundled lessons.mjs"
& $node (Join-Path $scriptDir "lessons.mjs")

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const OUT_DIRS = [path.join(ROOT, "content", "lessons"), path.join(ROOT, "public", "content", "lessons")];
let count = 0;
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
  const obj = objectives.map((o) => `- ${o}`).join("\n");
  const src = sources.map((s) => `- **${s[0]}**: ${s[1]}`).join("\n");
  const con = concepts.map((c) => `- **${c[0]}** — ${c[1]}.`).join("\n");
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
const LAB = "Лабораторная. Среда: **PostgreSQL**.";
const EX = "Итоговый тест части.";
const CMP = "> **Сравнение диалектов:** T-SQL (SQL Server) ↔ PostgreSQL\n";
const OPT = "> **Опционально:** задания можно выполнить на [MongoDB Playground](https://mongoplayground.net) без локальной установки.\n";
const LESSONS = {};

// ===== PART 6 =====
LESSONS["p6-l01-storage-arch"] = {
md: md("Архитектура хранения PostgreSQL", P6, M6, TH,
    ["Описать процессы postmaster и backend", "Объяснить shared buffers и WAL", "Наметить путь запроса к данным"],
    "PostgreSQL — **многопроцессная** СУБД. **Postmaster** принимает подключения и порождает **backend** (один на сессию). Фоновые процессы: checkpointer, walwriter, autovacuum, bgwriter.\r\n\r\n**Путь SELECT:** клиент → postmaster → backend → парсер/планировщик → исполнитель → **buffer manager** → страница из **shared_buffers** или с диска (8 КБ).\r\n\r\n**Shared buffers** — общий кэш страниц в RAM (`shared_buffers`, обычно ~25% RAM). **Buffer cache hit ratio** = blks_hit / (blks_hit + blks_read) — ключевой KPI.\r\n\r\n**WAL** — журнал упреждающей записи: изменения сначала в WAL, потом в data-файлы (durability, crash recovery).\r\n\r\n**Оптимизатор** выбирает план по статистике `pg_statistic`: nested loop, hash join, merge join — по оценке cost/rows (см. EXPLAIN).",
    [["morgunov", "Глава 18, §18.1"], ["novikov", "Глава 13, §13.1"]],
    [["Postmaster", "главный процесс кластера"], ["Shared buffers", "кэш страниц данных"],
     ["WAL", "журнал до записи в heap"], ["Backend", "процесс одной сессии"]]),

  quiz: quiz("p6-l01-storage-arch",
    sq("q1", "Кто принимает новые подключения?", ["Postmaster", "Walwriter", "Autovacuum", "Checkpointer"], 0, "Postmaster слушает порт."),
    sq("q2", "Shared buffers хранит…", ["Страницы таблиц и индексов", "Только WAL", "pg_hba.conf", "Пароли ролей"], 0, "Основной data cache."),
    sq("q3", "WAL нужен для…", ["Durability и recovery", "Только SELECT", "Создания VIEW", "Шифрования"], 0, "Write-Ahead Log."),
    sq("q4", "Buffer hit ratio растёт когда…", ["Больше чтений из RAM", "Отключён VACUUM", "Нет индексов", "wal_level=minimal"], 0, "blks_hit / (blks_hit+blks_read)."),
    mq("q5", "Фоновые процессы PostgreSQL? (верные)", ["Walwriter", "Checkpointer", "Autovacuum", "MongoDB router"], [0,1,2], "Стандартные фоновые workers.")),

  tasks: "## Задания\r\n\r\n1. Нарисуйте схему: клиент → postmaster → backend → shared_buffers → диск.\r\n2. ```sql\r\n   SELECT datname, blks_hit, blks_read,\r\n          round(100.0*blks_hit/nullif(blks_hit+blks_read,0),2) AS hit_pct\r\n   FROM pg_stat_database WHERE datname=current_database();\r\n   ```\r\n3. Объясните связь shared_buffers и latency SELECT.\r\n4. Прочитайте Morgunov §18.1.",
}

LESSONS["p6-l02-pages-tuples"] = {
md: md("Страницы, строки и HOT-обновления", P6, M6, TH,
    ["Описать структуру heap page", "Объяснить HOT и index-only scan", "Связать физику с производительностью"],
    "**Heap page** (8 КБ): заголовок, line pointers, **tuple** (строки). Tuple содержит xmin/xmax (MVCC) и данные.\r\n\r\n**UPDATE** создаёт новую версию tuple; старая — **dead tuple** → нужен VACUUM.\r\n\r\n**HOT (Heap-Only Tuple):** UPDATE без изменения индексированных столбцов, новая версия на той же странице — индексы не трогаем.\r\n\r\n**Index-Only Scan:** все столбцы в индексе + **visibility map** подтверждает видимость — heap не читается.\r\n\r\n**Алгоритмы JOIN:**\r\n\r\n| Алгоритм | Условие | I/O |\r\n|----------|---------|-----|\r\n| Nested Loop | Малая таблица + индекс | Random |\r\n| Hash Join | Равенство, влезает в work_mem | Seq + hash |\r\n| Merge Join | Отсортированные входы | Sequential |\r\n\r\n**FILLFACTOR 80** оставляет место для HOT на часто обновляемых таблицах (`performance`).",
    [["morgunov", "Глава 18, §18.2"], ["komarov", "Раздел 11: физическое хранение"]],
    [["Heap page", "8 КБ страница данных"], ["HOT", "update без обновления индексов"],
     ["Dead tuple", "устаревшая версия строки"], ["Visibility map", "карта видимых страниц"]]),

  quiz: quiz("p6-l02-pages-tuples",
    sq("q1", "Размер страницы по умолчанию?", ["8 КБ", "4 КБ", "16 КБ", "1 КБ"], 0, "BLCKSZ=8192."),
    sq("q2", "HOT возможен когда…", ["Не меняются индексированные столбцы", "Меняется PK", "Нет WAL", "Только DELETE"], 0, "Условия HOT."),
    sq("q3", "Hash Join выгоден при…", ["Equi-join и достаточно work_mem", "CROSS JOIN", "Нет статистики", "Только OUTER JOIN"], 0, "Hash по ключу равенства."),
    sq("q4", "Dead tuples появляются после…", ["UPDATE и DELETE", "SELECT", "CREATE INDEX", "GRANT"], 0, "MVCC версионирование."),
    mq("q5", "Index-Only Scan требует… (верные)", ["Covering index", "Актуальную visibility map", "CROSS JOIN", "Все столбцы в индексе"], [0,1,3], "Heap может не читаться.")),

  tasks: "## Задания\r\n\r\n1. Опишите структуру heap page.\r\n2. EXPLAIN (ANALYZE, BUFFERS) для JOIN student + performance — укажите тип join.\r\n3. Когда задать FILLFACTOR 70 для `performance`?\r\n4. Связь dead tuples и autovacuum.",
}

LESSONS["p6-l03-wal"] = {
md: md("Write-Ahead Log и контрольные точки", P6, M6, TH,
    ["Объяснить назначение WAL", "Настроить checkpoint и wal_level", "Понять crash recovery"],
    "**WAL:** сначала запись в журнал, затем в data-файлы. COMMIT подтверждается после fsync WAL.\r\n\r\nСегменты в `pg_wal/` (~16 МБ). **Checkpoint** сбрасывает dirty buffers, позволяет recycle WAL. Параметры: `checkpoint_timeout`, `max_wal_size`, `checkpoint_completion_target`.\r\n\r\n**Crash recovery:** redo WAL с последнего checkpoint; незавершённые TX — rollback.\r\n\r\n| wal_level | Применение |\r\n|-----------|------------|\r\n| minimal | Только recovery |\r\n| replica | Streaming replication, base backup |\r\n| logical | Logical replication |\r\n\r\nWAL — основа **репликации** и **PITR** (point-in-time recovery).",
    [["morgunov", "Глава 18, §18.3"], ["novikov", "Глава 13, §13.2"]],
    [["WAL", "журнал упреждающей записи"], ["Checkpoint", "точка сброса на диск"],
     ["LSN", "Log Sequence Number"], ["Redo", "повтор изменений при recovery"]]),

  quiz: quiz("p6-l03-wal",
    sq("q1", "Правило WAL?", ["Сначала WAL, потом data", "Сначала data", "WAL только чтение", "WAL=индекс"], 0, "Write-Ahead."),
    sq("q2", "wal_level=replica для…", ["Физической репликации", "Только VACUUM", "Отключения журнала", "MongoDB"], 0, "Streaming replication."),
    sq("q3", "Checkpoint…", ["Сбрасывает dirty pages", "Удаляет таблицы", "Создаёт роли", "Строит GIN"], 0, "Checkpointer process."),
    sq("q4", "При аварийном restart…", ["Replay WAL", "Пустая БД", "Только pg_dump", "Drop database"], 0, "Crash recovery."),
    mq("q5", "Параметры checkpoint? (верные)", ["max_wal_size", "checkpoint_timeout", "checkpoint_completion_target", "MongoDB port"], [0,1,2], "Настройка частоты CP.")),

  tasks: "## Задания\r\n\r\n1. Запишите wal_level, max_wal_size, checkpoint_timeout.\r\n2. `SELECT pg_current_wal_lsn(), pg_walfile_name(pg_current_wal_lsn());`\r\n3. Timeline: COMMIT → WAL → checkpoint → data files.\r\n4. Разница minimal vs replica vs logical.",
}

LESSONS["p6-l04-tablespaces"] = {
md: md("Tablespaces и размещение данных", P6, M6, SQL,
    ["Создать tablespace на отдельном диске", "Перенести индексы и таблицы", "Спланировать I/O нагрузку"],
    "**Tablespace** — имя → путь на диске. По умолчанию: `pg_default`, `pg_global`.\r\n\r\nЗачем: разделение I/O (SSD для индексов OLTP, HDD для архива), обслуживание без переустановки.\r\n\r\n```sql\r\nCREATE TABLESPACE fast_ssd LOCATION '/mnt/ssd/pgdata';\r\nCREATE INDEX idx ON performance(student_id) TABLESPACE fast_ssd;\r\nALTER TABLE archive_log SET TABLESPACE slow_hdd;\r\n```\r\n\r\nПлан: `student`, `performance` — быстрый диск; архив оценок — медленный.",
    [["morgunov", "Глава 19, §19.1"], ["komarov", "Раздел 12: tablespaces"]],
    [["Tablespace", "логическое размещение файлов"], ["pg_tablespace", "системный каталог"],
     ["I/O planning", "распределение по дискам"]]),

  quiz: quiz("p6-l04-tablespaces",
    sq("q1", "Tablespace — это…", ["Путь хранения файлов БД", "SQL-схема", "Тип JOIN", "WAL-сегмент"], 0, "Физическое размещение."),
    sq("q2", "CREATE INDEX ... TABLESPACE t1…", ["Кладёт файлы индекса в t1", "Создаёт VIEW", "Включает RLS", "Drop table"], 0, "Индексы тоже в tablespace."),
    sq("q3", "SSD для индексов OLTP…", ["Снижает random read latency", "Отключает WAL", "Заменяет VACUUM", "Только для TOAST"], 0, "Random I/O на SSD быстрее."),
    sq("q4", "DROP TABLESPACE требует…", ["Пустой tablespace", "pg_dump", "REINDEX ALL", "wal_level logical"], 0, "Все объекты перенесены."),
    mq("q5", "Сценарии tablespace? (верные)", ["Hot data SSD", "Archive HDD", "Разделение индексов", "Замена SQL"], [0,1,2], "Физическое tiering.")),

  tasks: "## Практика PostgreSQL\r\n\r\n1. `SELECT spcname, pg_tablespace_location(oid) FROM pg_tablespace;`\r\n2. Создайте tablespace (если есть каталог) и таблицу test_ts.\r\n3. Опишите размещение student vs performance_archive.\r\n4. Сохраните: `course/sql/p6-l04-tablespaces-solution.sql`",
}

LESSONS["p6-l05-toast"] = {
md: md("TOAST и хранение больших значений", P6, M6, TH,
    ["Объяснить механизм TOAST", "Выбрать стратегию storage для JSON/BLOB", "Диагностировать раздувание строк"],
    "**TOAST** — хранение значений > ~2 КБ вне основной страницы.\r\n\r\n| STORAGE | Поведение |\r\n|---------|-----------|\r\n| EXTENDED | Сжатие + out-of-line (default text/json) |\r\n| EXTERNAL | Out-of-line без сжатия |\r\n| MAIN | Сжатие, out-of-line если не влезает |\r\n| PLAIN | Без TOAST |\r\n\r\nБольшие JSON хранятся в **TOAST-таблице**; heap tuple — указатель. `pg_column_size(row)` — полный размер.\r\n\r\nРекомендации: не тащить BLOB в hot OLTP-row; GIN по нужным ключам JSON; редко обновляемые большие поля — в отдельную 1:1 таблицу.",
    [["morgunov", "Глава 19, §19.2"], ["novikov", "Глава 13, §13.3"]],
    [["TOAST", "oversized attribute storage"], ["Out-of-line", "данные вне heap page"],
     ["pg_column_size", "размер строки с TOAST"]]),

  quiz: quiz("p6-l05-toast",
    sq("q1", "TOAST активируется…", ["При больших значениях столбца", "При CREATE USER", "При JOIN", "При RLS"], 0, "Oversized attributes."),
    sq("q2", "EXTENDED стратегия…", ["Сжимает и выносит", "Запрещает NULL", "Создаёт BRIN", "WAL off"], 0, "Default для text."),
    sq("q3", "TOAST-данные лежат…", ["В отдельной TOAST-таблице", "В pg_hba", "В shared_buffers only", "В MongoDB"], 0, "Out-of-line storage."),
    sq("q4", "pg_column_size показывает…", ["Размер с TOAST", "Только PK", "Plan cost", "LSN"], 0, "Включая out-of-line."),
    mq("q5", "OLTP с большим JSON? (верные)", ["GIN по ключам", "Отдельная таблица", "Редкий UPDATE blob", "CROSS JOIN всего"], [0,1,2], "Минимизировать hot row width.")),

  tasks: "## Задания\r\n\r\n1. Таблица с text >100KB → pg_column_size().\r\n2. EXTENDED vs EXTERNAL — когда EXTERNAL?\r\n3. TOAST в схеме университета (описания курсов)?\r\n4. Связь TOAST-bloat и VACUUM.",
}

LESSONS["p6-l06-extensions"] = {
md: md("Расширения PostgreSQL: установка и обзор", P6, M6, SQL,
    ["Установить расширение через CREATE EXTENSION", "Использовать pg_trgm и uuid-ossp", "Оценить совместимость версий"],
    "**Extensions** — упакованные модули: типы, функции, операторы, FDW.\r\n\r\n```sql\r\nCREATE EXTENSION IF NOT EXISTS pg_trgm;\r\nCREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";\r\nCREATE EXTENSION IF NOT EXISTS pg_stat_statements;\r\n```\r\n\r\n**pg_trgm** — триграммы для LIKE/ similarity, GIN/GiST индексы нечёткого поиска.\r\n\r\n**uuid-ossp** — генерация UUID (`uuid_generate_v4()`).\r\n\r\n**pg_stat_statements** — топ SQL по времени/вызовам (нужен shared_preload_libraries).\r\n\r\n**Полнотекстовый поиск:**\r\n```sql\r\nCREATE EXTENSION pg_trgm; -- fuzzy\r\n-- tsvector/tsquery (встроено):\r\nSELECT to_tsvector('russian', 'база данных') @@ to_tsquery('russian', 'база');\r\nCREATE INDEX idx_fts ON docs USING GIN (to_tsvector('russian', body));\r\n```\r\n\r\nСовместимость: `SELECT * FROM pg_available_extensions;` — версия extension vs server.",
    [["morgunov", "Глава 20, §20.1"], ["komarov", "Раздел 13: extensions"]],
    [["CREATE EXTENSION", "установка модуля"], ["pg_trgm", "триграммный поиск"],
     ["tsvector", "лексемы полнотекстового поиска"], ["pg_stat_statements", "статистика SQL"]]),

  quiz: quiz("p6-l06-extensions",
    sq("q1", "CREATE EXTENSION…", ["Устанавливает модуль в БД", "Создаёт tablespace", "Drop WAL", "MongoDB sync"], 0, "Регистрация extension."),
    sq("q2", "pg_trgm для…", ["Нечёткого текстового поиска", "Replication", "Backup", "RLS"], 0, "Trigram similarity."),
    sq("q3", "GIN + to_tsvector…", ["Полнотекстовый индекс", "Hash join", "TOAST only", "Seq scan only"], 0, "FTS index."),
    sq("q4", "pg_stat_statements требует…", ["shared_preload_libraries", "wal_level minimal", "No indexes", "MongoDB"], 0, "Preload at startup."),
    mq("q5", "Популярные extensions? (верные)", ["pg_trgm", "uuid-ossp", "pg_stat_statements", "Cypher"], [0,1,2], "Стандартный набор DBA.")),

  tasks: "## Практика PostgreSQL\r\n\r\n1. `SELECT name, default_version FROM pg_available_extensions ORDER BY name LIMIT 20;`\r\n2. CREATE EXTENSION pg_trgm; — similarity('student','students').\r\n3. FTS: to_tsvector/to_tsquery по русскому тексту.\r\n4. Сохраните: `course/sql/p6-l06-extensions-solution.sql`",
}

LESSONS["p6-l07-monitoring-ext"] = {
md: md("Мониторинг: pg_stat и pg_stat_statements", P6, M6, SQL,
    ["Читать pg_stat_activity и pg_locks", "Найти долгие запросы", "Настроить pg_stat_statements"],
    "**pg_stat_activity** — активные сессии: state, query, wait_event, duration.\r\n\r\n```sql\r\nSELECT pid, usename, state, now()-query_start AS dur, left(query,80)\r\nFROM pg_stat_activity WHERE state <> 'idle' ORDER BY dur DESC;\r\n```\r\n\r\n**pg_locks** — блокировки; join с activity для диагностики deadlocks.\r\n\r\n**pg_stat_user_tables** — seq_scan vs idx_scan, n_live_tup, last_autovacuum.\r\n\r\n**pg_stat_statements** (extension):\r\n```sql\r\nSELECT calls, mean_exec_time, rows, left(query,100)\r\nFROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;\r\n```\r\n\r\n**Оптимизатор:** если seq_scan доминирует — нужны индексы; высокий mean_time — EXPLAIN ANALYZE, переписать JOIN, обновить статистику `ANALYZE`.\r\n\r\n**Buffer monitoring:** `pg_stat_bgwriter`, `pg_buffercache` (extension).",
    [["morgunov", "Глава 20, §20.2"], ["novikov", "Глава 14, §14.1"]],
    [["pg_stat_activity", "активные сессии"], ["pg_locks", "блокировки"],
     ["pg_stat_statements", "агрегат по SQL"], ["wait_event", "ожидание I/O/lock"]]),

  quiz: quiz("p6-l07-monitoring-ext",
    sq("q1", "Долгий запрос ищем в…", ["pg_stat_activity", "pg_hba.conf", "TOAST", "MongoDB"], 0, "query_start, state."),
    sq("q2", "pg_stat_statements показывает…", ["Топ SQL по времени", "Только DDL", "Только roles", "WAL size"], 0, "Aggregate query stats."),
    sq("q3", "seq_scan >> idx_scan означает…", ["Возможно нужны индексы", "Всё оптимально", "WAL broken", "RLS off"], 0, "Missing indexes hint."),
    sq("q4", "pg_locks + activity для…", ["Диагностики блокировок", "Backup", "FTS", "TOAST"], 0, "Lock troubleshooting."),
    mq("q5", "Действия при медленном query? (верные)", ["EXPLAIN ANALYZE", "ANALYZE table", "Проверить индексы", "Игнорировать"], [0,1,2], "Стандартный tuning flow.")),

  tasks: "## Практика PostgreSQL\r\n\r\n1. pg_stat_activity — найдите самый долгий active query.\r\n2. pg_stat_user_tables — seq_scan vs idx_scan для performance.\r\n3. Установите pg_stat_statements, top-5 по total_time.\r\n4. EXPLAIN ANALYZE медленного JOIN — предложите индекс.",
}

LESSONS["p6-l08-exam"] = {
md: md("Контроль: хранение и расширения PostgreSQL", P6, M6, EX,
    ["Объяснить путь записи на диск", "Спланировать tablespace", "Подключить расширение для задачи"],
    "Итоговый контроль части 6. Темы: архитектура процессов, страницы/MVCC/HOT, WAL/checkpoint, tablespaces, TOAST, extensions (pg_trgm, FTS), мониторинг pg_stat*.\r\n\r\n**Ключевые связи:** WAL → recovery/replication; shared_buffers → hit ratio; HOT/FILLFACTOR → UPDATE performance; pg_stat_statements → tuning; GIN+tsvector → полнотекстовый поиск.",
    [["morgunov", "Главы 18–20 (повторение)"], ["novikov", "Главы 13–14 (повторение)"]],
    [["Buffer pool", "shared_buffers"], ["WAL", "durability"], ["HOT", "update optimization"],
     ["Extensions", "модули PostgreSQL"]]),

  quiz: quiz("p6-l08-exam",
    sq("q1", "COMMIT гарантирует durability через…", ["WAL fsync", "Только shared_buffers", "TOAST", "pg_trgm"], 0, "WAL persistence."),
    sq("q2", "HOT снижает…", ["Нагрузку на индексы при UPDATE", "Размер WAL", "Need for SELECT", "Replication lag always"], 0, "Index updates skipped."),
    sq("q3", "Tablespace позволяет…", ["Разнести I/O по дискам", "Заменить JOIN", "Отключить MVCC", "MongoDB embed"], 0, "Physical placement."),
    sq("q4", "pg_stat_statements для…", ["Поиска тяжёлых запросов", "RLS policies", "TDE", "Graph traversal"], 0, "Query performance stats."),
    mq("q5", "Часть 6 охватывает? (верные)", ["Storage pages", "WAL", "Extensions/FTS", "Cypher only"], [0,1,2], "PostgreSQL internals.")),

  tasks: "## Итоговая работа\r\n\r\n1. Повторите уроки p6-l01 … p6-l07.\r\n2. Напишите эссе (1 стр.): путь INSERT от backend до диска через WAL.\r\n3. Схема tablespace для OLTP университета.\r\n4. Список 3 extensions для мониторинга + FTS + UUID.\r\n5. Пройдите все тесты части 6 (≥70%).",
}
// ===== PART 7 =====
LESSONS["p7-l01-auth"] = {
md: md("Аутентификация и pg_hba.conf", P7, M7, SQL,
    ["Настроить методы аутентификации", "Редактировать pg_hba.conf", "Подключиться с SSL-сертификатом"],
    "**Аутентификация** — кто вы; **авторизация** — что вам можно (GRANT, RLS).\r\n\r\n**pg_hba.conf** — правила подключения (Host-Based Authentication):\r\n\r\n```\r\n// TYPE  DATABASE  USER  ADDRESS       METHOD\r\nlocal   all       all                 peer\r\nhost    mydb      app   10.0.0.0/24   scram-sha-256\r\nhostssl all       all   0.0.0.0/0     cert\r\n```\r\n\r\nМетоды: **trust**, **peer** (local), **md5/scram-sha-256**, **cert** (SSL client cert).\r\n\r\nПосле изменения: `pg_ctl reload` или `SELECT pg_reload_conf();`\r\n\r\n**SSL in transit:** `ssl=on`, сертификаты в postgresql.conf; клиент `sslmode=verify-full`.\r\n\r\nРоли ≠ пользователи ОС: `CREATE ROLE app_user LOGIN PASSWORD '...';`",
    [["morgunov", "Глава 21, §21.1"], ["novikov", "Глава 15, §15.1"]],
    [["pg_hba.conf", "правила аутентификации"], ["SCRAM-SHA-256", "современный hash пароля"],
     ["sslmode", "режим SSL клиента"]]),

  quiz: quiz("p7-l01-auth",
    sq("q1", "pg_hba.conf определяет…", ["Правила подключения", "План JOIN", "TOAST", "ETL"], 0, "HBA rules."),
    sq("q2", "scram-sha-256 — это…", ["Метод аутентификации", "Тип индекса", "WAL level", "OLAP cube"], 0, "Password auth."),
    sq("q3", "hostssl требует…", ["SSL-соединение", "Local socket only", "No password", "MongoDB"], 0, "Encrypted transport."),
    sq("q4", "После правки pg_hba…", ["pg_reload_conf()", "DROP DATABASE", "VACUUM FULL", "CREATE EXTENSION"], 0, "Reload config."),
    mq("q5", "Методы auth? (верные)", ["peer", "scram-sha-256", "cert", "hash join"], [0,1,2], "Auth methods.")),

  tasks: "## Практика PostgreSQL\r\n\r\n1. Найдите pg_hba.conf (`SHOW hba_file;`).\r\n2. Создайте роль `readonly` с LOGIN.\r\n3. Добавьте правило (в тестовой среде) для scram-sha-256.\r\n4. Опишите sslmode=verify-full vs require.",
}

LESSONS["p7-l02-roles"] = {
md: md("Роли, привилегии GRANT и REVOKE", P7, M7, SQL,
    ["Создать роли и назначить права", "Ограничить доступ к схемам и таблицам", "Применить принцип наименьших привилегий"],
    "PostgreSQL: **ROLE** = пользователь или группа. `CREATE ROLE`, `GRANT`, `REVOKE`.\r\n\r\n```sql\r\nCREATE ROLE analyst NOLOGIN;\r\nGRANT CONNECT ON DATABASE university TO analyst;\r\nGRANT USAGE ON SCHEMA public TO analyst;\r\nGRANT SELECT ON student, s_group TO analyst;\r\nGRANT analyst TO user_ivan;  -- membership\r\nREVOKE INSERT ON performance FROM analyst;\r\n```\r\n\r\n**Привилегии:** SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER, CREATE, USAGE.\r\n\r\n**Схемы:** `GRANT USAGE ON SCHEMA` — вход в схему; затем права на объекты.\r\n\r\n**Default privileges:** `ALTER DEFAULT PRIVILEGES` для будущих таблиц.\r\n\r\n**Least privilege:** приложению — только нужные DML; DBA — отдельная роль; не использовать superuser в app.",
    [["morgunov", "Глава 21, §21.2"], ["petkovic", "Глава 9: безопасность"]],
    [["GRANT", "выдача прав"], ["REVOKE", "отзыв прав"], ["ROLE", "пользователь/группа"],
     ["Least privilege", "минимально необходимые права"]]),

  quiz: quiz("p7-l02-roles",
    sq("q1", "GRANT SELECT ON t TO r даёт…", ["Чтение таблицы t роли r", "INSERT", "Superuser", "WAL admin"], 0, "SELECT privilege."),
    sq("q2", "NOLOGIN роль…", ["Групповая роль", "Superuser only", "Cannot GRANT", "MongoDB role"], 0, "Group role pattern."),
    sq("q3", "USAGE ON SCHEMA нужен для…", ["Доступа к объектам схемы", "Backup", "Replication", "TOAST"], 0, "Schema access."),
    sq("q4", "Least privilege означает…", ["Минимум прав для задачи", "ALL PRIVILEGES всем", "Trust auth", "No RLS"], 0, "Security principle."),
    mq("q5", "Привилегии таблицы? (верные)", ["SELECT", "INSERT", "UPDATE", "MERGE only Mongo"], [0,1,2], "Table privileges.")),

  tasks: "## Практика PostgreSQL\r\n\r\n1. CREATE ROLE app_read NOLOGIN; GRANT SELECT на student, s_group.\r\n2. CREATE USER app1 LOGIN PASSWORD 'test'; GRANT app_read TO app1;\r\n3. Проверьте: app1 может SELECT, не может INSERT.\r\n4. REVOKE и проверка снова.",
}

LESSONS["p7-l03-rls"] = {
md: md("Row-Level Security (RLS)", P7, M7, SQL,
    ["Включить RLS на таблице", "Написать политику USING/WITH CHECK", "Протестировать изоляцию строк"],
    "**RLS** — фильтрация строк по политикам на уровне СУБД (не только в приложении).\r\n\r\n```sql\r\nALTER TABLE performance ENABLE ROW LEVEL SECURITY;\r\nCREATE POLICY perf_student ON performance\r\n  FOR SELECT TO student_role\r\n  USING (student_id = current_setting('app.student_id')::int);\r\nCREATE POLICY perf_ins ON performance FOR INSERT TO student_role\r\n  WITH CHECK (student_id = current_setting('app.student_id')::int);\r\n```\r\n\r\n**USING** — какие строки видны; **WITH CHECK** — какие можно вставить/обновить.\r\n\r\n**BYPASSRLS** — атрибут роли (админ); **SECURITY DEFINER** функции — осторожно.\r\n\r\nСравнение с SQL Server: там тоже RLS (security predicates); в PostgreSQL — policies на таблице.",
    [["morgunov", "Глава 21, §21.3"], ["pro-tsql", "Глава 15: RLS в SQL Server"]],
    [["RLS", "безопасность на уровне строк"], ["USING", "фильтр чтения"],
     ["WITH CHECK", "ограничение записи"], ["Policy", "именованное правило"]]),

  quiz: quiz("p7-l03-rls",
    sq("q1", "RLS включается…", ["ALTER TABLE ... ENABLE ROW LEVEL SECURITY", "CREATE INDEX", "VACUUM", "TOAST"], 0, "Enable RLS."),
    sq("q2", "USING определяет…", ["Видимые строки", "Только INSERT", "WAL level", "Backup"], 0, "Read filter."),
    sq("q3", "WITH CHECK для…", ["INSERT/UPDATE ограничений", "SELECT only", "DROP", "Replication"], 0, "Write filter."),
    sq("q4", "BYPASSRLS позволяет…", ["Обходить RLS", "Только read", "MongoDB sync", "FTS"], 0, "Admin bypass."),
    mq("q5", "RLS vs app filter? (верные)", ["RLS в СУБД", "Сложнее обойти", "Нужны policies", "Заменяет GRANT"], [0,1,2], "Defense in depth.")),

  tasks: "## Практика PostgreSQL\r\n\r\n1. ENABLE RLS на performance для роли student.\r\n2. Policy: студент видит только свои оценки (через session variable).\r\n3. SET app.student_id; SELECT — проверка изоляции.\r\n4. Сравните с RLS в SQL Server (pro-tsql ch.15).",
}

LESSONS["p7-l04-encryption"] = {
md: md("Шифрование: at rest и in transit", P7, M7, TH,
    ["Настроить SSL для подключений", "Объяснить TDE и pgcrypto", "Выбрать стратегию защиты данных"],
    "**In transit:** TLS между клиентом и PostgreSQL (`ssl=on`, `hostssl` в pg_hba). Защита от перехвата паролей/данных в сети.\r\n\r\n**At rest:**\r\n- **Файловая/дисковая** encryption (LUKS, BitLocker, cloud volume encryption) — прозрачно для PG.\r\n- **TDE** (Transparent Data Encryption) — в SQL Server нативно; в PostgreSQL — через OS/disk или pg_tde extensions (сторонние).\r\n- **pgcrypto** — шифрование столбцов: `pgp_sym_encrypt(data, key)`, хранение ciphertext.\r\n\r\n```sql\r\nCREATE EXTENSION pgcrypto;\r\nINSERT INTO secrets(val) VALUES (pgp_sym_encrypt('text', 'key'));\r\nSELECT pgp_sym_decrypt(val::bytea, 'key') FROM secrets;\r\n```\r\n\r\n**Ключи:** не в коде; vault/HSM; rotation policy.\r\n\r\n**CAP-контекст:** шифрование не заменяет backup/replication; согласованность и доступность — отдельные оси.",
    [["novikov", "Глава 15, §15.2"], ["komarov", "Раздел 14: шифрование"]],
    [["TLS", "шифрование канала"], ["At rest", "шифрование на диске"],
     ["pgcrypto", "шифрование столбцов"], ["TDE", "прозрачное шифрование БД"]]),

  quiz: quiz("p7-l04-encryption",
    sq("q1", "SSL/TLS защищает…", ["Данные in transit", "At rest only", "Только indexes", "WAL internal"], 0, "Network encryption."),
    sq("q2", "pgcrypto для…", ["Шифрования столбцов", "Hash join", "Replication", "VACUUM"], 0, "Column-level crypto."),
    sq("q3", "TDE в SQL Server…", ["Transparent disk encryption", "Only MongoDB", "No PostgreSQL analog native", "Both B and C partly true"], 3, "PG: OS/disk or extensions."),
    sq("q4", "Ключи шифрования…", ["Хранить в vault, не в коде", "В pg_hba.conf", "In plain SQL", "Public repo"], 0, "Key management."),
    mq("q5", "Defense layers? (верные)", ["TLS", "Disk encryption", "Column encrypt", "Disable auth"], [0,1,2], "Layered security.")),

  tasks: "## Задания\r\n\r\n1. Опишите три уровня: TLS, disk encryption, pgcrypto column.\r\n2. Когда column encryption vs disk encryption?\r\n3. Сравните TDE SQL Server и подход PostgreSQL.\r\n4. Риски хранения ключей в приложении.",
}

LESSONS["p7-l05-backup"] = {
md: md("Резервное копирование: pg_dump и pg_basebackup", P7, M7, SQL,
    ["Сделать логический дамп pg_dump", "Выполнить физический base backup", "Восстановить БД из резервной копии"],
    "**Логический backup — pg_dump:**\r\n```bash\r\npg_dump -Fc -f university.dump university_db\r\npg_restore -d university_new university.dump\r\n```\r\nПортативный, выборочный; медленнее на huge DB.\r\n\r\n**Физический — pg_basebackup:**\r\n```bash\r\npg_basebackup -D /backup/base -Ft -z -P\r\n```\r\nКопия data directory + WAL для PITR. Требует wal_level=replica, replication slot.\r\n\r\n**PITR:** archive_mode + restore_command → recovery до точки во времени.\r\n\r\n**Стратегия:** RPO/RTO; ежедневный dump + continuous WAL archive; тест restore регулярно.\r\n\r\n**pg_dump --schema-only** для DDL; **--data-only** для данных.",
    [["morgunov", "Глава 22, §22.1"], ["petkovic", "Глава 10: backup"]],
    [["pg_dump", "логический дамп"], ["pg_basebackup", "физическая копия"],
     ["PITR", "восстановление на момент времени"], ["RPO/RTO", "допустимая потеря/простой"]]),

  quiz: quiz("p7-l05-backup",
    sq("q1", "pg_dump создаёт…", ["Логический дамп", "Physical only", "WAL segment", "MongoDB export"], 0, "Logical backup."),
    sq("q2", "pg_basebackup нужен wal_level…", ["replica или выше", "minimal only", "off", "Mongo"], 0, "For physical replication backup."),
    sq("q3", "PITR использует…", ["Base backup + WAL archive", "Only pg_dump", "Only TRUNCATE", "RLS"], 0, "Point-in-time recovery."),
    sq("q4", "pg_restore -d для…", ["Восстановления custom dump", "DELETE all", "CREATE USER", "ANALYZE"], 0, "Restore into DB."),
    mq("q5", "Backup best practices? (верные)", ["Test restore", "WAL archiving", "Offsite copy", "Never test"], [0,1,2], "Backup hygiene.")),

  tasks: "## Практика PostgreSQL\r\n\r\n1. pg_dump -Fc вашей учебной БД.\r\n2. pg_restore в новую БД test_restore.\r\n3. Сравните размер custom vs plain SQL dump.\r\n4. Опишите RPO/RTO для университета (оценки).",
}

LESSONS["p7-l06-replication"] = {
md: md("Репликация: streaming и logical", P7, M7, SQL,
    ["Настроить streaming replication", "Объяснить logical replication", "Спланировать failover"],
    "**Streaming (physical):** standby получает WAL потоком; побайтовая копия кластера.\r\n\r\nPrimary: `wal_level=replica`, `max_wal_senders`, replication role.\r\nStandby: `primary_conninfo`, `hot_standby=on`.\r\n\r\n**Logical replication:** публикация/подписка на уровне таблиц; cross-version, selective.\r\n\r\n```sql\r\nCREATE PUBLICATION pub_perf FOR TABLE performance;\r\nCREATE SUBSCRIPTION sub_perf CONNECTION '...' PUBLICATION pub_perf;\r\n```\r\n\r\n**Failover:** Patroni, repmgr, manual promote. **CAP:** при partition сеть — выбор CP vs AP (PostgreSQL sync rep → CP bias).\r\n\r\n**Read replicas:** отчёты на standby, снижение нагрузки на primary (OLAP на replica).",
    [["morgunov", "Глава 22, §22.2"], ["novikov", "Глава 16, §16.1"]],
    [["Streaming replication", "физическая WAL-репликация"], ["Logical replication", "табличная публикация"],
     ["Standby", "реplica-сервер"], ["Failover", "переключение primary"]]),

  quiz: quiz("p7-l06-replication",
    sq("q1", "Streaming replication передаёт…", ["WAL поток", "Only SQL queries", "MongoDB oplog", "CSV"], 0, "Physical WAL stream."),
    sq("q2", "Logical replication…", ["Выборочные таблицы", "Full cluster byte copy only", "No WAL", "Only backup"], 0, "Table-level pub/sub."),
    sq("q3", "hot_standby позволяет…", ["SELECT на replica", "Write on standby", "No connection", "Drop primary"], 0, "Read-only queries."),
    sq("q4", "Synchronous replication улучшает…", ["Durability (RPO)", "Write speed always", "No lag ever guaranteed", "MongoDB"], 0, "Commit waits for standby."),
    mq("q5", "Failover planning? (верные)", ["Monitoring lag", "Promotion procedure", "Split-brain prevention", "Ignore WAL"], [0,1,2], "HA planning.")),

  tasks: "## Задания\r\n\r\n1. Опишите архитектуру primary + 1 standby.\r\n2. Logical vs streaming — когда что?\r\n3. Что такое replication lag и как мониторить?\r\n4. Связь replication и CAP (partition tolerance).",
}

LESSONS["p7-l07-oltp-olap"] = {
md: md("OLTP vs OLAP: сравнение нагрузок", P7, M7, TH,
    ["Различить транзакционную и аналитическую нагрузку", "Сопоставить нормализацию и денormalization", "Выбрать архитектуру под сценарий"],
    "**OLTP:** много коротких транзакций (INSERT оценки, UPDATE профиля). 3NF, индексы на PK/FK, row-level locks, low latency.\r\n\r\n**OLAP:** тяжёлые read, агрегаты, scan больших объёмов. Star schema, denormalized dimensions, columnar (ClickHouse, etc.), batch load.\r\n\r\n| | OLTP | OLAP |\r\n|---|------|------|\r\n| Запросы | Короткие точечные | Scan + GROUP BY |\r\n| Схема | Нормализованная | Star/snowflake |\r\n| Consistency | Strong ACID | Often eventual in loads |\r\n| Пример | university OLTP | DWH успеваемости |\r\n\r\n**CAP (Brewer):** в partition — выбор **C** (consistency) vs **A** (availability). PostgreSQL sync rep → CP; async → AP bias с lag.\r\n\r\n**HTAP:** гибриды (PostgreSQL + columnar extension) — компромисс.\r\n\r\nАрхитектура: OLTP → ETL/CDC → DWH для отчётов; не гонять OLAP на primary без replica.",
    [["lecture1", "Слайды 80–95"], ["smirnov", "Глава 1: OLTP и OLAP"]],
    [["OLTP", "транзакционная нагрузка"], ["OLAP", "аналитическая нагрузка"],
     ["CAP", "consistency/availability/partition"], ["Denormalization", "для аналитики"]]),

  quiz: quiz("p7-l07-oltp-olap",
    sq("q1", "OLTP характеризуется…", ["Много коротких транзакций", "Только batch scan", "No indexes", "Only CSV"], 0, "Transactional workload."),
    sq("q2", "OLAP часто использует…", ["Star schema", "3NF only", "No aggregation", "MongoDB only"], 0, "Dimensional model."),
    sq("q3", "CAP: при partition сеть…", ["Trade-off C vs A", "Both always", "Neither", "WAL off"], 0, "Partition tolerance forces choice."),
    sq("q4", "OLAP на primary OLTP…", ["Плохая идея без replica", "Always best", "Required", "Replaces backup"], 0, "Separate workloads."),
    mq("q5", "OLTP design? (верные)", ["Normalization", "Indexes on FK", "Short transactions", "Full table scan reports"], [0,1,2], "OLTP patterns.")),

  tasks: "## Задания\r\n\r\n1. Классифицируйте: «вставить оценку» vs «средний балл по факультетам за 5 лет».\r\n2. Нарисуйте OLTP → ETL → DWH для университета.\r\n3. Объясните CAP на примере async replication.\r\n4. Когда star schema вместо 3NF?",
}

LESSONS["p7-l08-exam"] = {
md: md("Контроль: безопасность, резервирование и OLTP/OLAP", P7, M7, EX,
    ["Спроектировать модель доступа", "Выполнить backup/restore", "Обосновать выбор OLTP или OLAP"],
    "Итог части 7: pg_hba/auth, GRANT/REVOKE, RLS, encryption, pg_dump/basebackup, replication, OLTP/OLAP/CAP.\r\n\r\nКомплексный сценарий: учебная БД университета — роли (student/teacher/admin), RLS на performance, backup policy, read replica для отчётов.",
    [["morgunov", "Главы 21–22 (повторение)"], ["novikov", "Главы 15–16 (повторение)"]],
    [["GRANT", "авторизация"], ["RLS", "строки"], ["Backup", "pg_dump/PITR"], ["Replication", "HA/read scale"]]),

  quiz: quiz("p7-l08-exam",
    sq("q1", "Студент видит только свои строки…", ["RLS policy", "CROSS JOIN", "TOAST", "BRIN only"], 0, "Row security."),
    sq("q2", "pg_dump vs basebackup…", ["Logical vs physical", "Same thing", "Only Mongo", "Only WAL"], 0, "Backup types."),
    sq("q3", "Least privilege…", ["Минимум прав", "ALL to PUBLIC", "trust all", "No roles"], 0, "Security."),
    sq("q4", "Async replication CAP…", ["AP with lag", "Always CP", "No partition", "No WAL"], 0, "Availability bias."),
    mq("q5", "Часть 7 topics? (верные)", ["Security", "Backup", "Replication OLTP/OLAP", "Graph Cypher only"], [0,1,2], "Admin topics.")),

  tasks: "## Итоговая работа\r\n\r\n1. Модель ролей: admin, teacher, student для university DB.\r\n2. RLS: student → только свои performance.\r\n3. pg_dump + restore test.\r\n4. Схема primary + replica для отчётов.\r\n5. Эссе: OLTP vs OLAP для деканата.",
}

// ===== PART 8 =====
LESSONS["p8-l01-dwh-concepts"] = {
md: md("Хранилища данных: понятия и архитектура", P8, M8, TH,
    ["Определить DWH, Data Mart и Data Lake", "Описать слои staging и core", "Сопоставить Inmon и Kimball"],
    "**DWH (Data Warehouse)** — предметно-ориентированное, интегрированное, неvolatile, time-variant хранилище для аналитики (Inmon).\r\n\r\n**Data Mart** — витрина под департамент (продажи, успеваемость).\r\n\r\n**Data Lake** — сырьё (raw files) в object storage; schema-on-read.\r\n\r\n**Слои:**\r\n- **Staging** — сырые копии из источников (OLTP).\r\n- **Core/Integration** — очистка, conform dimensions (Inmon bus architecture).\r\n- **Presentation** — star schemas, marts, reports.\r\n\r\n**Inmon:** сверху-вниз, normalized enterprise DWH → marts.\r\n**Kimball:** снизу-вверх, dimensional star schemas по процессам (факты + измерения).\r\n\r\nДля **университета:** источник — OLTP (student, performance); DWH — история успеваемости, агрегаты по группам/кафедрам.",
    [["smirnov", "Глава 1–2"], ["lecture1", "Слайды 96–110"]],
    [["DWH", "аналитическое хранилище"], ["Staging", "промежуточная зона"],
     ["Inmon", "корпоративное DWH"], ["Kimball", "dimensional modeling"]]),

  quiz: quiz("p8-l01-dwh-concepts",
    sq("q1", "DWH отличается от OLTP…", ["Ориентация на аналитику", "Только INSERT", "No history", "3NF forbidden"], 0, "Analytical focus."),
    sq("q2", "Kimball фокус…", ["Star schemas / dimensions", "Only 6NF", "MongoDB", "No facts"], 0, "Dimensional."),
    sq("q3", "Staging layer…", ["Сырые данные из источников", "Final reports", "OLTP transactions", "WAL"], 0, "Landing zone."),
    sq("q4", "Data Mart…", ["Subject-area subset", "Full lake only", "Replacing OLTP", "pg_hba"], 0, "Department mart."),
    mq("q5", "DWH properties? (верные)", ["Integrated", "Time-variant", "Non-volatile", "Real-time OLTP only"], [0,1,2], "Inmon criteria.")),

  tasks: "## Задания\r\n\r\n1. Сравните Inmon и Kimball (таблица 5 строк).\r\n2. Нарисуйте слои: OLTP → staging → core → mart для университета.\r\n3. Data Lake vs DWH — когда lake?\r\n4. Прочитайте Smirnov гл. 1–2.",
}

LESSONS["p8-l02-dimensional"] = {
md: md("Измерения и факты: основы dimensional modeling", P8, M8, TH,
    ["Выделить fact и dimension таблицы", "Определить grain фактовой таблицы", "Спроектировать surrogate key"],
    "**Fact table** — метрики (measures): оценка, сумма продаж, количество. **Grain** — что означает одна строка («одна оценка студента за экзамен»).\r\n\r\n**Dimension** — контекст: студент, время, дисциплина, группа. Denormalized атрибуты для удобства фильтрации.\r\n\r\n**Surrogate key** — искусственный PK dimension (student_key), отдельно от business key (student_id из OLTP).\r\n\r\n**Types of facts:** additive (sum), semi-additive (balance), non-additive (ratio).\r\n\r\nПример университета:\r\n- Fact: `fact_performance` (student_key, date_key, subject_key, grade)\r\n- Dim: `dim_student`, `dim_date`, `dim_subject`\r\n\r\n**Slowly Changing Dimensions (SCD):** Type 1 overwrite; Type 2 history rows with effective dates.",
    [["smirnov", "Глава 3"], ["info-support", "Раздел 5: измерения"]],
    [["Fact", "таблица метрик"], ["Dimension", "контекст анализа"],
     ["Grain", "детализация строки факта"], ["Surrogate key", "суррогатный ключ"]]),

  quiz: quiz("p8-l02-dimensional",
    sq("q1", "Grain факта — это…", ["Что описывает одна строка", "PK dimension", "WAL size", "Index type"], 0, "Fact granularity."),
    sq("q2", "Surrogate key…", ["Искусственный PK dimension", "Business natural key only", "WAL LSN", "Mongo _id only"], 0, "Warehouse PK."),
    sq("q3", "Оценка в fact table — …", ["Measure", "Dimension", "Staging", "pg_hba"], 0, "Numeric measure."),
    sq("q4", "SCD Type 2…", ["История изменений dimension", "Overwrite", "Delete all", "No dates"], 0, "Historical tracking."),
    mq("q5", "Dimension содержит… (верные)", ["Descriptive attributes", "Filters for reports", "Surrogate key", "Only WAL"], [0,1,2], "Dimension role.")),

  tasks: "## Задания\r\n\r\n1. Для fact «продажи» определите grain.\r\n2. dim_student: какие атributы (имя, группа, факультет)?\r\n3. SCD: студент перевёлся в другую группу — Type 1 vs 2?\r\n4. Surrogate vs natural key — зачем surrogate?",
}

LESSONS["p8-l03-star-schema"] = {
md: md("Звезда (Star Schema)", P8, M8, TH,
    ["Построить star schema для продаж", "Денormalize измерения", "Оценить производительность запросов"],
    "**Star schema:** центральная **fact** + **dimensions** вокруг (радиальная схема). Dimensions **denormalized** (все атрибуты группы в dim_student).\r\n\r\n```\r\n        dim_date\r\n            |\r\ndim_student — fact_performance — dim_subject\r\n            |\r\n        dim_group\r\n```\r\n\r\n**Плюсы:** простые JOIN, быстрые агрегаты для BI, понятно бизнесу.\r\n**Минусы:** redundancy в dimensions, риск inconsistency без ETL discipline.\r\n\r\n**Запрос:** средний балл по факультетам за семестр — JOIN fact + dim_student + dim_date, GROUP BY faculty.\r\n\r\n**Университет (design task):** grain = одна оценка; facts: grade, attempt; dims: student (name, group_id, faculty), date (semester, year), subject (name, department).",
    [["smirnov", "Глава 4, §4.1"], ["practicum", "Глава 8: star schema"]],
    [["Star schema", "fact + denormalized dims"], ["Fact table", "центр звезды"],
     ["Denormalization", "для скорости чтения"]],
    "\nСквозная предметная область: **университет** — звезда для успеваемости.\n"),

  quiz: quiz("p8-l03-star-schema",
    sq("q1", "Star schema имеет…", ["Одну fact и несколько dimensions", "Только 3NF", "No facts", "Graph edges"], 0, "Star pattern."),
    sq("q2", "Dimensions в star…", ["Denormalized", "Always 5NF", "No attributes", "Only PK"], 0, "Wide dimensions."),
    sq("q3", "Fact_performance grain…", ["Одна оценка за экзамен", "Весь студент", "Вся группа", "WAL record"], 0, "Fine-grained fact."),
    sq("q4", "Star vs OLTP 3NF…", ["Star for read analytics", "Star for OLTP writes", "Identical", "No JOINs in star"], 0, "Analytical optimization."),
    mq("q5", "Star query pattern? (верные)", ["JOIN fact to dims", "GROUP BY dim attrs", "Filter on dimensions", "Only CROSS JOIN"], [0,1,2], "Typical BI query.")),

  tasks: "## Задания — проектирование star schema университета\r\n\r\n**Обязательное задание:** спроектируйте star schema для аналитики успеваемости.\r\n\r\n1. **Fact table** `fact_grade` — определите grain и measures (grade, credits, is_pass).\r\n2. **Dimensions:** `dim_student`, `dim_group`, `dim_subject`, `dim_date`, `dim_department`.\r\n3. Для каждой dimension перечислите 5+ атрибутов (denormalized где нужно).\r\n4. Нарисуйте диаграмму звезды (draw.io).\r\n5. Напишите SQL-запрос: средний балл по кафедрам за 2024–2025 уч. год.\r\n6. Обоснуйте выбор grain и surrogate keys.",
}

LESSONS["p8-l04-snowflake"] = {
md: md("Снежинка (Snowflake Schema)", P8, M8, TH,
    ["Нормализовать измерения в snowflake", "Сравнить star и snowflake", "Выбрать схему для ETL"],
    "**Snowflake** — dimensions **нормализованы** в иерархии:\r\n\r\n```\r\ndim_group → dim_faculty → dim_university\r\nfact → dim_student → dim_group → ...\r\n```\r\n\r\n**Star vs Snowflake:**\r\n\r\n| | Star | Snowflake |\r\n|---|------|-----------|\r\n| Dimensions | Flat wide | Normalized chains |\r\n| JOIN count | Меньше | Больше |\r\n| Storage | Больше redundancy | Меньше |\r\n| ETL | Проще load wide | Сложнее maintain FKs |\r\n| BI tools | Предпочитают star | Extra joins |\r\n\r\nДля **университета:** snowflake если faculty/university shared across marts и нужна строгая конformность; star — если скорость разработки важнее.\r\n\r\nKimball: обычно star; snowflake — когда dimensions очень большие или shared conformed dimensions (Inmon bus).",
    [["smirnov", "Глава 4, §4.2"], ["komarov", "Раздел 15: snowflake"]],
    [["Snowflake schema", "нормализованные dimensions"], ["Conformed dimension", "общее измерение"],
     ["Hierarchy", "faculty → university"]]),

  quiz: quiz("p8-l04-snowflake",
    sq("q1", "Snowflake отличается…", ["Нормализованные dimensions", "No fact table", "Only MongoDB", "WAL"], 0, "Normalized dims."),
    sq("q2", "Star проще для…", ["BI users и queries", "Only ETL", "Write OLTP", "Backup"], 0, "Fewer joins."),
    sq("q3", "Snowflake снижает…", ["Redundancy in dims", "All JOINs", "Need for facts", "Storage always zero"], 0, "Normalized storage."),
    sq("q4", "Conformed dimension…", ["Одинаковое измерение в marts", "Unique to one fact", "OLTP only", "pg_trgm"], 0, "Shared dim."),
    mq("q5", "Choose snowflake when? (верные)", ["Large shared hierarchies", "Storage cost matters", "Strict conformity", "Always over star"], [0,1,2], "Trade-offs.")),

  tasks: "## Задания\r\n\r\n1. Перерисуйте star universiteta v snowflake (faculty отдельно).\r\n2. Сосчитайте JOIN для «средний балл по faculty» в star vs snowflake.\r\n3. Когда выбрали бы star для деканата?\r\n4. Smirnov §4.2.",
}

LESSONS["p8-l05-etl"] = {
md: md("ETL и ELT: загрузка данных в DWH", P8, M8, TH,
    ["Описать этапы extract, transform, load", "Сравнить ETL и ELT", "Спроектировать staging area"],
    "**ETL:** Extract (OLTP, APIs) → Transform (cleanse, conform, surrogate keys) → Load (fact/dim).\r\n\r\n**ELT:** Extract → Load raw to staging (cloud DWH) → Transform in SQL (BigQuery, Snowflake).\r\n\r\n**Staging area:** копии source tables; validation; audit columns (load_date, batch_id).\r\n\r\n**Steps для university DWH:**\r\n1. Extract student, performance из PostgreSQL OLTP.\r\n2. Transform: lookup surrogate keys, handle SCD Type 2 для student.\r\n3. Load fact_grade, refresh dim_*.\r\n\r\n**Quality:** dedup, null checks, FK integrity, reconciliation counts.\r\n\r\n**Tools:** pg_dump/COPY, Apache Airflow, dbt, custom Python/SQL scripts.\r\n\r\nSmirnov: медленно меняющиеся измерения, late arriving facts, incremental load.",
    [["smirnov", "Глава 5"], ["lecture1", "Слайды 111–120"]],
    [["ETL", "extract-transform-load"], ["Staging", "промежуточная область"],
     ["Incremental load", "дельта-загрузка"], ["dbt", "transform in warehouse"]]),

  quiz: quiz("p8-l05-etl",
    sq("q1", "Extract в ETL…", ["Читает источники", "Only BI", "Drop DWH", "VACUUM"], 0, "Source read."),
    sq("q2", "ELT transform…", ["В хранилище после load", "Before extract", "Never", "Only Mongo"], 0, "Transform in DWH."),
    sq("q3", "Staging для…", ["Валидации и audit", "Final reports only", "OLTP writes", "RLS"], 0, "Landing/QA."),
    sq("q4", "Surrogate keys назначаются…", ["В transform", "In OLTP only", "Never", "pg_hba"], 0, "DW transform step."),
    mq("q5", "ETL quality checks? (верные)", ["Row counts", "Null keys", "Duplicate detection", "Ignore all"], [0,1,2], "Data quality.")),

  tasks: "## Задания\r\n\r\n1. Опишите ETL pipeline OLTP performance → fact_grade (5 шагов).\r\n2. Incremental vs full load — когда что?\r\n3. SCD Type 2 при ETL смены группы студента.\r\n4. Reconciliation: count OLTP vs fact.",
}

LESSONS["p8-l06-olap-cubes"] = {
md: md("OLAP-кубы и операции drill-down", P8, M8, TH,
    ["Выполнить slice, dice, roll-up", "Объяснить ROLAP vs MOLAP", "Построить простой OLAP-отчёт"],
    "**OLAP operations:**\r\n- **Slice** — фиксируем одно измерение (semester=1).\r\n- **Dice** — подcube по нескольким фильтрам.\r\n- **Roll-up** — агрегация вверх (день → месяц → год).\r\n- **Drill-down** — детализация (faculty → group → student).\r\n\r\n**ROLAP:** SQL over star schema (PostgreSQL, ClickHouse).\r\n**MOLAP:** precomputed cube (SSAS, Essbase) — быстрый, less flexible.\r\n**HOLAP:** hybrid.\r\n\r\nSQL roll-up:\r\n```sql\r\nSELECT d.year, d.semester, avg(f.grade)\r\nFROM fact_grade f\r\nJOIN dim_date d ON f.date_key = d.date_key\r\nGROUP BY ROLLUP (d.year, d.semester);\r\n```\r\n\r\nSmirnov: куб = метрика по осям dimensions; pivot tables в Excel — простой OLAP UI.",
    [["smirnov", "Глава 6"], ["novikov", "Глава 17, §17.2"]],
    [["Slice/Dice", "выбор подмножества куба"], ["Roll-up", "агрегация"],
     ["ROLAP", "SQL-based OLAP"], ["MOLAP", "multidimensional storage"]]),

  quiz: quiz("p8-l06-olap-cubes",
    sq("q1", "Roll-up…", ["Агрегирует к более coarse grain", "Details only", "DELETE facts", "WAL"], 0, "Aggregation up."),
    sq("q2", "Drill-down…", ["Детализация", "Delete dim", "Backup", "RLS"], 0, "More detail."),
    sq("q3", "ROLAP использует…", ["Relational star schema", "Only binary cube", "MongoDB only", "No SQL"], 0, "SQL OLAP."),
    sq("q4", "GROUP BY ROLLUP…", ["Иерархические subtotals", "Only one row", "CROSS JOIN", "TOAST"], 0, "SQL rollup."),
    mq("q5", "OLAP ops? (верные)", ["Slice", "Dice", "Pivot", "VACUUM"], [0,1,2], "Classic ops.")),

  tasks: "## Задания\r\n\r\n1. Slice: только spring semester — SQL filter.\r\n2. Roll-up: оценки year → semester → month (если есть date dim).\r\n3. ROLAP vs MOLAP для университета?\r\n4. Smirnov гл. 6.",
}

LESSONS["p8-l07-data-marts"] = {
md: md("Витрины данных (Data Marts)", P8, M8, TH,
    ["Спроектировать subject-area mart", "Определить SLA обновления", "Интегрировать mart с DWH"],
    "**Data Mart** — subset DWH для одной предметной области (деанат, admissions, finance).\r\n\r\n**Dependent mart** — из enterprise DWH (Inmon).\r\n**Independent mart** — Kimball standalone star для быстрого старта.\r\n\r\n**SLA:** nightly batch vs hourly incremental; freshness vs cost.\r\n\r\n**University marts:**\r\n- **Mart успеваемости** — fact_grade + dims; users: деканат.\r\n- **Mart контингента** — dim_student snapshots; users: учебный отдел.\r\n\r\n**Integration:** conformed dimensions (dim_date, dim_student) across marts для cross-reporting.\r\n\r\n**Security:** mart-level GRANT; row filters по faculty (аналог RLS в presentation layer).",
    [["smirnov", "Глава 7"], ["info-support", "Раздел 6: витрины"]],
    [["Data Mart", "предметная витрина"], ["SLA", "соглашение о свежести"],
     ["Conformed dimension", "сквозное измерение"]]),

  quiz: quiz("p8-l07-data-marts",
    sq("q1", "Data Mart…", ["Subject-area analytics", "OLTP system", "WAL archive", "Mongo only"], 0, "Department focus."),
    sq("q2", "Conformed dim…", ["Shared across marts", "Unique name only", "No surrogate", "Staging only"], 0, "Enterprise consistency."),
    sq("q3", "SLA defines…", ["Refresh frequency/latency", "SQL dialect", "Index type", "TOAST"], 0, "Service level."),
    sq("q4", "Dependent mart sources…", ["Enterprise DWH", "Only Excel", "Never ETL", "pg_hba"], 0, "Top-down Inmon."),
    mq("q5", "Mart design? (верные)", ["Clear users", "Defined grain", "Refresh policy", "No facts"], [0,1,2], "Mart checklist.")),

  tasks: "## Задания\r\n\r\n1. Опишите mart для деканата факультета IT (tables, users, SLA nightly).\r\n2. Какие conformed dimensions с mart контингента?\r\n3. Independent vs dependent mart — пример.\r\n4. Smirnov гл. 7.",
}

LESSONS["p8-l08-dwh-lab"] = {
md: md("Кейс: проектирование хранилища продаж", P8, M8, LAB,
    ["Построить star schema для retail", "Написать ETL-скрипт загрузки", "Сформировать аналитический отчёт"],
    "**Лабораторная:** retail sales DWH (Smirnov практика) + параллельно **university star** из p8-l03.\r\n\r\n**Retail star:**\r\n- fact_sales (sale_id grain): quantity, amount, discount\r\n- dim_product, dim_customer, dim_store, dim_date\r\n\r\n**ETL sketch (PostgreSQL staging):**\r\n```sql\r\nCREATE TABLE stg_sales AS SELECT * FROM oltp.sales WHERE sale_date >= current_date - 1;\r\nINSERT INTO fact_sales SELECT ... surrogate lookups ... FROM stg_sales;\r\n```\r\n\r\n**Отчёт:** выручка по магазинам и категориям за месяц.\r\n\r\n**University extension:** fact_grade + dims; отчёт — топ-5 групп по среднему баллу.",
    [["smirnov", "Глава 8 (практика)"], ["practicum", "Задание 8: DWH"]],
    [["Retail star", "fact_sales"], ["ETL script", "staging to fact"], ["BI report", "GROUP BY aggregates"]]),

  quiz: quiz("p8-l08-dwh-lab",
    sq("q1", "fact_sales grain…", ["Одна строка продажи", "Весь магазин", "One day all sales", "Student"], 0, "Line item sale."),
    sq("q2", "Staging перед load…", ["Validate source data", "Replace OLTP", "Skip transform", "WAL only"], 0, "QA layer."),
    sq("q3", "Surrogate lookup в ETL…", ["JOIN dim by business key", "Random UUID only", "No dims", "CROSS JOIN"], 0, "Key mapping."),
    sq("q4", "Отчёт retail…", ["SUM(amount) BY store", "Only INSERT", "VACUUM", "RLS"], 0, "Aggregate report."),
    mq("q5", "Lab deliverables? (верные)", ["Star diagram", "ETL SQL", "Analytical query", "Mongo install"], [0,1,2], "Lab outputs.")),

  tasks: "## Лабораторная\r\n\r\n**Retail (Smirnov):**\r\n1. Star schema: fact_sales + 4 dimensions (diagram).\r\n2. DDL PostgreSQL для fact и dims.\r\n3. ETL: stg → fact (INSERT script).\r\n4. Отчёт: revenue by store, month.\r\n\r\n**University (дополнительно):**\r\n5. Star schema успеваемости (из p8-l03).\r\n6. SQL: top-5 групп по avg(grade).\r\n\r\nСохраните: `course/sql/p8-l08-dwh-lab.sql`",
}

LESSONS["p8-l09-exam"] = {
md: md("Контроль: проектирование хранилищ данных", P8, M8, EX,
    ["Спроектировать dimensional model", "Обосновать выбор star/snowflake", "Описать pipeline загрузки данных"],
    "Итог части 8: Inmon/Kimball, facts/dimensions/grain, star/snowflake, ETL/ELT, OLAP ops, marts.\r\n\r\n**Экзаменационный кейс:** университет — построить DWH успеваемости: star schema, ETL из OLTP, OLAP запрос (roll-up по faculty), SLA mart для деканата.",
    [["smirnov", "Главы 1–8 (повторение)"], ["lecture1", "Слайды 96–120 (повторение)"]],
    [["Dimensional model", "facts+dims"], ["Star", "denormalized"], ["ETL", "pipeline"], ["OLAP", "slice/roll-up"]]),

  quiz: quiz("p8-l09-exam",
    sq("q1", "Kimball акцент…", ["Dimensional stars", "Only 6NF OLTP", "Mongo only", "No ETL"], 0, "Kimball method."),
    sq("q2", "Grain определяет…", ["Строку fact", "WAL", "Index", "Role"], 0, "Fact row meaning."),
    sq("q3", "Star для university grades…", ["fact_grade + dims", "Only OLTP 3NF", "Graph DB", "pg_hba"], 0, "Analytical schema."),
    sq("q4", "Roll-up in SQL…", ["GROUP BY coarser dim", "DELETE", "TRUNCATE staging", "RLS off"], 0, "Aggregation."),
    mq("q5", "Part 8 topics? (верные)", ["Inmon/Kimball", "ETL", "Star schema", "PostgreSQL WAL only"], [0,1,2], "DWH topics.")),

  tasks: "## Итоговая работа\r\n\r\n1. Полный dimensional design university DWH (diagram + DDL).\r\n2. Star vs snowflake — обоснование.\r\n3. ETL pipeline (10 шагов).\r\n4. 3 OLAP запроса: slice, roll-up, drill-down.\r\n5. Все тесты части 8 ≥70%.",
}

// ===== PART 9 =====
LESSONS["p9-l01-nosql-overview"] = {
md: md("NoSQL: обзор моделей и сценариев", P9, M9A, TH,
    ["Классифицировать document, key-value, graph, column", "Сопоставить NoSQL и реляционные БД", "Выбрать технологию под use case"],
    "**NoSQL** — не «no SQL», а «not only SQL»; отказ от строгой relational модели ради scale/flexibility.\r\n\r\n| Модель | Пример | Use case |\r\n|--------|--------|----------|\r\n| Document | MongoDB | JSON catalog, CMS |\r\n| Key-value | Redis | Cache, sessions |\r\n| Column-family | Cassandra | Time series, wide rows |\r\n| Graph | Neo4j | Social, fraud, paths |\r\n\r\n**vs RDBMS:** схема гибкая vs rigid; horizontal scale vs vertical; eventual consistency vs ACID (часто); JOIN expensive vs normalized.\r\n\r\n**Когда PostgreSQL достаточно:** JSONB + GIN, pgvector, ltree — «SQL + extensions».\r\n\r\n**Когда MongoDB:** nested documents, rapid schema change, shard by access pattern.\r\n\r\n**Когда Graph:** many-hop relationships (friends-of-friends), shortest path — JOIN hell в SQL.",
    [["mongodb", "Глава 1"], ["graph-db", "Глава 1"]],
    [["Document DB", "JSON/BSON documents"], ["Key-value", "K-V store"],
     ["Graph DB", "vertices and edges"], ["CAP", "trade-offs at scale"]]),

  quiz: quiz("p9-l01-nosql-overview",
    sq("q1", "Document DB хранит…", ["JSON/BSON documents", "Only tables 3NF", "WAL only", "pg_hba"], 0, "Document model."),
    sq("q2", "Graph DB силён в…", ["Path traversal", "Simple ledger OLTP only", "Only backup", "FTS"], 0, "Relationship queries."),
    sq("q3", "Redis — …", ["Key-value store", "Relational", "Column DWH", "WAL"], 0, "In-memory KV."),
    sq("q4", "PostgreSQL JSONB…", ["Hybrid document in SQL", "Replaces Mongo always", "No indexes", "Graph native"], 0, "JSON in RDBMS."),
    mq("q5", "NoSQL fit? (верные)", ["Flexible schema", "Horizontal scale", "Specific access patterns", "Always replace PG"], [0,1,2], "Selective use.")),

  tasks: "## Задания\r\n\r\n1. Классифицируйте: каталог товаров, кэш сессий, social network, OLTP банк.\r\n2. Когда university OLTP остаётся в PostgreSQL?\r\n3. Сравните CAP для Cassandra vs PostgreSQL sync rep.\r\n4. MongoDB + Graph DB гл. 1.",
}

LESSONS["p9-l02-mongo-model"] = {
md: md("MongoDB: документная модель и BSON", P9, M9A, TH,
    ["Описать коллекции и документы", "Спроектировать вложенную схему", "Сравнить embedding и referencing"],
    "**MongoDB:** database → **collection** → **document** (BSON). Нет фиксированной схемы (flexible schema).\r\n\r\n```json\r\n{\r\n  \"_id\": ObjectId(\"...\"),\r\n  \"student_id\": 101,\r\n  \"name\": \"Иванов\",\r\n  \"group\": { \"code\": \"ИВТ-21\", \"faculty\": \"IT\" },\r\n  \"grades\": [ { \"subject\": \"БД\", \"score\": 5 } ]\r\n}\r\n```\r\n\r\n**Embedding** — вложенные массивы/объекты: один read, atomic update документа; но document size limit 16MB, duplication.\r\n\r\n**Referencing** — `$lookup` или manual refs like SQL FK: normalization, smaller docs; нужны доп. queries.\r\n\r\n**vs PostgreSQL JSONB:** Mongo — native sharding, aggregation pipeline; PG — ACID, JOIN, один стек.\r\n\r\n" + OPT,
    [["mongodb", "Главы 2–3"], ["komarov", "Раздел 16: document DB"]],
    [["Collection", "набор документов"], ["BSON", "binary JSON"],
     ["Embedding", "вложение данных"], ["Referencing", "ссылки между docs"]]),

  quiz: quiz("p9-l02-mongo-model",
    sq("q1", "MongoDB document…", ["BSON record in collection", "SQL table row only", "WAL segment", "Index only"], 0, "Document unit."),
    sq("q2", "Embedding подходит…", ["One-to-few nested data", "Unlimited 100MB arrays", "Cross-shard JOIN", "Graph paths"], 0, "Bounded nesting."),
    sq("q3", "_id в MongoDB…", ["Primary key document", "Foreign key only", "WAL LSN", "Schema name"], 0, "Default PK."),
    sq("q4", "Referencing vs embedding…", ["Normalize vs denormalize trade-off", "Same always", "No choice", "PG only"], 0, "Modeling choice."),
    mq("q5", "Mongo design? (верные)", ["Access pattern first", "16MB doc limit", "Shard key matters", "Always 3NF"], [0,1,2], "Document modeling.")),

  tasks: "## Задания (опционально — без установки MongoDB)\r\n\r\n" + OPT + "\r\n1. Спроектируйте document для student+grades: embedding vs referencing — 2 варианта JSON.\r\n2. Когда embedding grades в student doc?\r\n3. Эквивалент PostgreSQL: JSONB column vs normalized tables.\r\n4. MongoDB Playground: создайте sample document (опционально).",
}

LESSONS["p9-l03-mongo-queries"] = {
md: md("MongoDB: CRUD и запросы", P9, M9A, TH,
    ["Выполнить find, insert, update, delete", "Использовать операторы $gt, $in, $regex", "Создать индексы в MongoDB"],
    "**CRUD (MongoDB shell / driver):**\r\n\r\n```javascript\r\ndb.students.insertOne({ name: \"Петров\", group: \"ИВТ-21\" })\r\ndb.students.find({ \"grades.score\": { $gt: 4 } })\r\ndb.students.updateOne({ name: \"Петров\" }, { $set: { status: \"active\" } })\r\ndb.students.deleteMany({ status: \"inactive\" })\r\n```\r\n\r\n**Operators:** `$gt`, `$gte`, `$in`, `$regex`, `$elemMatch`.\r\n\r\n**Indexes:** `db.students.createIndex({ group: 1, name: 1 })`\r\n\r\n**PostgreSQL equivalent:**\r\n\r\n| Mongo | PostgreSQL |\r\n|-------|------------|\r\n| find({a:1}) | SELECT * WHERE a=1 |\r\n| $gt | > |\r\n| $in | IN (...) |\r\n| insertOne | INSERT ... RETURNING |\r\n| updateOne $set | UPDATE ... SET |\r\n\r\n" + OPT,
    [["mongodb", "Главы 4–5"], ["practicum", "Задание 9: MongoDB"]],
    [["find", "query documents"], ["$operators", "filter operators"], ["createIndex", "index in Mongo"]]),

  quiz: quiz("p9-l03-mongo-queries",
    sq("q1", "find({score: {$gt: 4}})…", ["score > 4", "score = 4", "score < 4", "DELETE"], 0, "$gt greater than."),
    sq("q2", "$in в Mongo…", ["Match any in list", "Index only", "JOIN", "WAL"], 0, "IN equivalent."),
    sq("q3", "updateOne…", ["Updates first match", "All documents always", "Drop collection", "CREATE TABLE"], 0, "Single doc update."),
    sq("q4", "PG equivalent find filter…", ["WHERE clause", "GROUP BY", "VACUUM", "GRANT"], 0, "SQL WHERE."),
    mq("q5", "Mongo CRUD? (верные)", ["insertOne", "find", "updateOne", "MERGE native"], [0,1,2], "Basic ops.")),

  tasks: "## Задания (опционально)\r\n\r\n" + OPT + "\r\n1. Запишите find для students с grade > 4 в группе ИВТ-21.\r\n2. PG equivalent: SELECT с WHERE и JOIN.\r\n3. Какие индексы для { group: 1, \"grades.score\": 1 }?\r\n4. Playground: выполните insert + find (опционально).",
}

LESSONS["p9-l04-mongo-aggregation"] = {
md: md("MongoDB: aggregation pipeline", P9, M9A, TH,
    ["Построить pipeline $match, $group, $lookup", "Сформировать аналитический отчёт", "Сравнить с SQL GROUP BY"],
    "**Aggregation pipeline** — stages left-to-right:\r\n\r\n```javascript\r\ndb.performance.aggregate([\r\n  { $match: { year: 2025 } },\r\n  { $group: { _id: \"$group\", avgGrade: { $avg: \"$grade\" } } },\r\n  { $sort: { avgGrade: -1 } },\r\n  { $lookup: { from: \"groups\", localField: \"_id\", foreignField: \"code\", as: \"g\" } }\r\n])\r\n```\r\n\r\n**Stages:** $match (filter), $group (aggregate), $project, $lookup (left join), $unwind (flatten array).\r\n\r\n**SQL equivalent:**\r\n```sql\r\nSELECT group_id, avg(grade) FROM performance WHERE year=2025 GROUP BY group_id ORDER BY 2 DESC;\r\n-- $lookup ≈ LEFT JOIN\r\n```\r\n\r\nДля DWH-grade analytics часто проще SQL/star schema; Mongo aggregation — когда data already in documents.\r\n\r\n" + OPT,
    [["mongodb", "Глава 6"], ["headfirst", "Приложение: NoSQL"]],
    [["$match", "filter stage"], ["$group", "aggregation"], ["$lookup", "join-like stage"]]),

  quiz: quiz("p9-l04-mongo-aggregation",
    sq("q1", "$group похож на…", ["SQL GROUP BY", "CREATE INDEX", "VACUUM", "RLS"], 0, "Aggregation."),
    sq("q2", "$lookup…", ["Join-like between collections", "Delete", "Insert only", "WAL"], 0, "Left outer join."),
    sq("q3", "$match первым для…", ["Reduce documents early", "Slow query", "No reason", "Backup"], 0, "Filter early."),
    sq("q4", "$avg в $group…", ["Average measure", "Primary key", "Index type", "Shard key"], 0, "Aggregator."),
    mq("q5", "Pipeline stages? (верные)", ["$match", "$group", "$lookup", "$CHECKPOINT"], [0,1,2], "Common stages.")),

  tasks: "## Задания (опционально)\r\n\r\n" + OPT + "\r\n1. Pipeline: avg grade by group, top 5.\r\n2. SQL equivalent с GROUP BY и ORDER BY.\r\n3. Когда star schema лучше aggregation Mongo?\r\n4. Playground pipeline (опционально).",
}

LESSONS["p9-l05-graph-intro"] = {
md: md("Графовые базы данных: модель и применение", P9, M9A, TH,
    ["Определить вершины, рёбра и свойства", "Привести примеры social и fraud graphs", "Оценить преимущества перед RDBMS"],
    "**Property Graph:** **vertices (nodes)** + **edges (relationships)** + properties on both.\r\n\r\nПримеры:\r\n- **Social:** Person —FRIEND→ Person; recommendation, communities.\r\n- **Fraud:** Account —TRANSFER→ Account; cycle detection, mule networks.\r\n- **University:** Student —ENROLLED→ Course —TAUGHT_BY→ Teacher; prerequisites chain.\r\n\r\n**vs RDBMS:** recursive CTE в SQL для graphs возможен, но multi-hop (6+) дорог (JOIN explosion). Graph DB: **index-free adjacency**, native traversal O(edges) not O(rows).\r\n\r\n**Neo4j, Amazon Neptune, etc.** — Cypher, Gremlin query languages.\r\n\r\n**When not graph:** simple FK relationships, reporting aggregates — PostgreSQL достаточно.",
    [["graph-db", "Главы 2–3"], ["komarov", "Раздел 17: graph DB"]],
    [["Vertex", "узел графа"], ["Edge", "relationship"], ["Traversal", "обход графа"],
     ["Index-free adjacency", "быстрый local hop"]]),

  quiz: quiz("p9-l05-graph-intro",
    sq("q1", "Graph DB vertex…", ["Node/entity", "SQL table only", "WAL", "Index B-tree only"], 0, "Node."),
    sq("q2", "Edge represents…", ["Relationship", "Primary key", "Backup", "Schema"], 0, "Relationship."),
    sq("q3", "Multi-hop friends…", ["Graph traversal", "CROSS JOIN only", "TRUNCATE", "TOAST"], 0, "Path query."),
    sq("q4", "Fraud ring detection…", ["Graph pattern match", "Only COUNT(*)", "VACUUM", "pg_dump"], 0, "Pattern in graph."),
    mq("q5", "Graph fit? (верные)", ["Social networks", "Path finding", "Network topology", "Simple ledger 2 tables"], [0,1,2], "Graph use cases.")),

  tasks: "## Задания\r\n\r\n1. Нарисуйте graph: Student-Course-Teacher для университета.\r\n2. SQL recursive CTE vs graph — 3-hop friends, что проще?\r\n3. Fraud: найти cycle transfers — почему graph?\r\n4. Graph DB гл. 2–3.",
}

LESSONS["p9-l06-graph-queries"] = {
md: md("Graph DB: Cypher и обход графа", P9, M9A, TH,
    ["Написать MATCH и RETURN в Cypher", "Выполнить k-hop обход", "Сравнить производительность с JOIN"],
    "**Cypher (Neo4j):**\r\n\r\n```cypher\r\nMATCH (s:Student {name: 'Иванов'})-[:ENROLLED]->(c:Course)\r\nRETURN c.name, c.credits\r\n\r\nMATCH (a:Person)-[:FRIEND*1..3]-(b:Person)\r\nWHERE a.name = 'Alice'\r\nRETURN DISTINCT b.name\r\n\r\nMATCH path = (s:Student)-[:PREREQ*]->(c:Course {name: 'БД'})\r\nRETURN path\r\n```\r\n\r\n**k-hop:** variable length `[*1..k]` — друзья до 3 уровня.\r\n\r\n**vs SQL:**\r\n```sql\r\nWITH RECURSIVE hops AS (\r\n  SELECT friend_id, 1 AS depth FROM friends WHERE user_id = 1\r\n  UNION ALL\r\n  SELECT f.friend_id, h.depth+1 FROM friends f JOIN hops h ON f.user_id = h.friend_id WHERE h.depth < 3\r\n) SELECT * FROM hops;\r\n```\r\n\r\nGraph wins on deep/varied traversals; SQL wins on aggregates over star schema.\r\n\r\nОпционально: [Neo4j Browser sandbox](https://sandbox.neo4j.com) без локальной установки.",
    [["graph-db", "Главы 4–5"], ["mongodb", "Глава 7 (сравнение)"]],
    [["Cypher", "язык запросов Neo4j"], ["MATCH", "pattern matching"], ["Variable-length path", "k-hop traversal"]]),

  quiz: quiz("p9-l06-graph-queries",
    sq("q1", "MATCH (a)-[:KNOWS]->(b)…", ["Directed pattern", "INSERT only", "DROP", "VACUUM"], 0, "Pattern syntax."),
    sq("q2", "[:FRIEND*1..3]…", ["1 to 3 hops", "Exactly 1", "Infinite only", "No path"], 0, "Variable length."),
    sq("q3", "RETURN in Cypher…", ["Output columns", "Delete all", "Create index", "Grant"], 0, "Projection."),
    sq("q4", "Deep traversal SQL…", ["Recursive CTE", "Simple JOIN once", "TRUNCATE", "TOAST"], 0, "SQL recursion."),
    mq("q5", "Cypher patterns? (верные)", ["Node label :Student", "Relationship :KNOWS", "Property filter {name:'X'}", "TABLESPACE"], [0,1,2], "Cypher elements.")),

  tasks: "## Задания (опционально — Neo4j sandbox)\r\n\r\n1. Cypher: все курсы студента Иванов.\r\n2. 2-hop friends of Alice.\r\n3. SQL recursive equivalent для 2-hop.\r\n4. Когда JOIN 10 tables хуже graph traversal?",
}

LESSONS["p9-l07-tsql-overview"] = {
md: md("T-SQL: обзор для PostgreSQL-разработчика", P9, M9B,
    CMP + "\nПрактика: сравнение синтаксиса; PostgreSQL — основная среда курса.",
    ["Сопоставить синтаксис T-SQL и PostgreSQL", "Использовать TOP и OFFSET/FETCH", "Применить переменные и batch"],
    "**T-SQL** — диалект Microsoft SQL Server. Курс использует PostgreSQL; этот урок — **сравнение диалектов**.\r\n\r\n| Задача | T-SQL | PostgreSQL |\r\n|--------|-------|------------|\r\n| Top N | `SELECT TOP 10 * FROM t` | `SELECT * FROM t LIMIT 10` |\r\n| Pagination | `OFFSET 10 ROWS FETCH NEXT 5 ROWS ONLY` | `LIMIT 5 OFFSET 10` |\r\n| String concat | `'a' + 'b'` | `'a' \\|\\| 'b'` or concat() |\r\n| Identity | `IDENTITY(1,1)` | `SERIAL` / `GENERATED ALWAYS AS IDENTITY` |\r\n| Boolean | `BIT` | `BOOLEAN` |\r\n| Date | `GETDATE()` | `now()` / `CURRENT_TIMESTAMP` |\r\n| Batch | `GO` separator | Single transaction / `;` |\r\n\r\n**Variables:**\r\n```sql\r\n-- T-SQL\r\nDECLARE @x INT = 5;\r\n-- PostgreSQL\r\nDO $$ DECLARE x int := 5; BEGIN ... END $$;\r\n```\r\n\r\n**Schemas:** SQL Server dbo vs PostgreSQL public.",
    [["ben-gan", "Главы 1–3"], ["petkovic", "Главы 1–4"]],
    [["TOP", "T-SQL limit rows"], ["LIMIT", "PostgreSQL limit"], ["GO", "batch separator SSMS"],
     ["IDENTITY", "auto-increment T-SQL"]]),

  quiz: quiz("p9-l07-tsql-overview",
    sq("q1", "TOP 10 in T-SQL ≈ PG…", ["LIMIT 10", "OFFSET 10", "FETCH WAL", "TOP is PG native"], 0, "LIMIT equivalent."),
    sq("q2", "GETDATE() in PG…", ["now() or CURRENT_TIMESTAMP", "GETDATE()", "SYSDATE only", "No dates"], 0, "Timestamp functions."),
    sq("q3", "GO in SSMS…", ["Batch separator not SQL", "Transaction commit", "CREATE INDEX", "RLS"], 0, "Client directive."),
    sq("q4", "IDENTITY ≈ PG…", ["SERIAL / GENERATED IDENTITY", "UUID only", "MANUAL only", "TOAST"], 0, "Auto increment."),
    mq("q5", "Dialect diffs? (верные)", ["TOP vs LIMIT", "+ vs \|\| concat", "BIT vs BOOLEAN", "Identical MERGE syntax always"], [0,1,2], "Compare dialects.")),

  tasks: "## Задания — сравнение диалектов\r\n\r\n" + CMP + "\r\n1. Перепишите T-SQL `SELECT TOP 5 name FROM student ORDER BY name` → PostgreSQL.\r\n2. Pagination: OFFSET/FETCH (T-SQL) vs LIMIT/OFFSET (PG) — один запрос, два варианта.\r\n3. DECLARE variable: напишите оба синтаксиса.\r\n4. Таблица: 5 отличий T-SQL vs PostgreSQL из опыта.",
}

LESSONS["p9-l08-tsql-advanced"] = {
md: md("T-SQL: процедуры, функции и MERGE", P9, M9B,
    CMP + "\nСравнение продвинутых конструкций T-SQL и PostgreSQL.",
    ["Написать stored procedure в T-SQL", "Использовать MERGE для upsert", "Применить error handling TRY/CATCH"],
    "**Stored procedures:**\r\n\r\n```sql\r\n-- T-SQL\r\nCREATE PROC dbo.UpsertGrade @sid INT, @grade INT AS\r\nBEGIN TRY\r\n  MERGE performance AS t USING (SELECT @sid AS sid) s ON t.student_id = s.sid\r\n  WHEN MATCHED THEN UPDATE SET grade = @grade\r\n  WHEN NOT MATCHED THEN INSERT (student_id, grade) VALUES (@sid, @grade);\r\nEND TRY\r\nBEGIN CATCH\r\n  THROW;\r\nEND CATCH\r\n\r\n-- PostgreSQL\r\nCREATE OR REPLACE PROC upsert_grade(p_sid int, p_grade int)\r\nLANGUAGE plpgsql AS $$\r\nBEGIN\r\n  INSERT INTO performance (student_id, grade) VALUES (p_sid, p_grade)\r\n  ON CONFLICT (student_id) DO UPDATE SET grade = EXCLUDED.grade;\r\nEXCEPTION WHEN OTHERS THEN RAISE;\r\nEND; $$;\r\n```\r\n\r\n| Feature | T-SQL | PostgreSQL |\r\n|---------|-------|------------|\r\n| MERGE | Native MERGE (2019+) | INSERT ON CONFLICT |\r\n| Error handling | TRY/CATCH | EXCEPTION block |\r\n| Procedures | CREATE PROC | CREATE PROCEDURE (PG14+) |\r\n| Table variables | @t TABLE | TEMP TABLE |\r\n| Output inserted | OUTPUT clause | RETURNING |",
    [["ben-gan", "Главы 10–11"], ["pro-tsql", "Главы 5–7"]],
    [["MERGE", "upsert T-SQL"], ["ON CONFLICT", "upsert PostgreSQL"],
     ["TRY/CATCH", "T-SQL errors"], ["RETURNING", "PG output clause"]]),

  quiz: quiz("p9-l08-tsql-advanced",
    sq("q1", "MERGE in PG often replaced by…", ["INSERT ON CONFLICT", "TOP 10", "CROSS JOIN", "VACUUM"], 0, "Upsert pattern."),
    sq("q2", "TRY/CATCH ≈ PG…", ["BEGIN ... EXCEPTION", "Only GO", "pg_hba", "WAL"], 0, "Exception handling."),
    sq("q3", "OUTPUT inserted in T-SQL ≈…", ["RETURNING in PG", "LIMIT", "TOAST", "RLS"], 0, "Returning rows."),
    sq("q4", "CREATE PROC in PG since…", ["v14+ procedures", "Never", "Only Mongo", "v8 only"], 0, "SQL procedures."),
    mq("q5", "Upsert options? (верные)", ["T-SQL MERGE", "PG ON CONFLICT", "Manual IF EXISTS", "Only TRUNCATE"], [0,1,2], "Upsert patterns.")),

  tasks: "## Задания — сравнение диалектов\r\n\r\n" + CMP + "\r\n1. MERGE/upsert grade для student_id — T-SQL и PG версии.\r\n2. TRY/CATCH (T-SQL) vs EXCEPTION (PG) — пример деления на ноль.\r\n3. OUTPUT vs RETURNING после INSERT.\r\n4. Когда портировать proc с T-SQL на PL/pgSQL — checklist (5 пунктов).",
}

LESSONS["p9-l09-date-advanced"] = {
md: md("К. Дж. Дейт: продвинутая реляционная теория", P9, M9B, TH,
    ["Обсудить NULL и реляционную модель", "Разобрать view updating problem", "Оценить соответствие SQL теории"],
    "**К. Дж. Дейт** критически оценивает SQL с позиции реляционной теории.\r\n\r\n**NULL:** SQL ternary logic (TRUE/FALSE/UNKNOWN); Date: NULL нарушает информационную целостность — «missing» vs «not applicable»; рекомендация — избегать NULL, использовать домены и DEFAULT или отдельные таблицы.\r\n\r\n**View updating problem:** не все VIEW обновляемы; JOIN view, aggregation view — неоднозначность какую base table обновлять. SQL1999+ CHECK OPTION, INSTEAD OF triggers; PostgreSQL — rules, triggers.\r\n\r\n**Duplicate rows:** SQL bag semantics (multiset) vs relational set; DISTINCT «латание».\r\n\r\n**Foreign key actions:** theory vs CASCADE практика.\r\n\r\n**The Third Manifesto / Tutorial D:** альтернатива SQL (не промышленный стандарт, но учит мыслить реляционно).\r\n\r\n**PostgreSQL:** близок к SQL standard, но extensions (JSONB, arrays) — pragmatic departure.\r\n\r\nЧитать: Date «SQL and Relational Theory», главы о NULL, views, constraints.",
    [["date-sql", "Главы 11–14"], ["date-intro", "Главы 19–21"]],
    [["NULL problem", "трёхзначная логика"], ["View updating", "обновление представлений"],
     ["Bag vs set", "дубликаты в SQL"], ["Relational fidelity", "соответствие теории"]]),

  quiz: quiz("p9-l09-date-advanced",
    sq("q1", "Date criticizes NULL because…", ["Ambiguous meaning", "Too fast", "No indexes", "WAL"], 0, "Semantic ambiguity."),
    sq("q2", "View with GROUP BY update…", ["Generally not updatable", "Always simple", "Auto MERGE", "Mongo only"], 0, "Updating problem."),
    sq("q3", "SQL bags vs sets…", ["SQL allows duplicates without DISTINCT", "SQL is always set", "No difference", "PG only"], 0, "Multiset semantics."),
    sq("q4", "INSTEAD OF trigger helps…", ["Updatable complex views", "Backup", "Replication", "TOAST"], 0, "View update workaround."),
    mq("q5", "Date themes? (верные)", ["NULL critique", "View updating", "Relational purity", "Replace all SQL with Mongo"], [0,1,2], "Theory topics.")),

  tasks: "## Задания\r\n\r\n1. Пример WHERE unknown (NULL comparison) — SQL behavior.\r\n2. Создайте VIEW с JOIN — почему INSERT ambiguous?\r\n3. DISTINCT: когда «костыль» vs legitimate?\r\n4. Date гл. 11–14: 3 тезиса своими словами.\r\n5. PostgreSQL JSONB — departure from pure relational? аргументы.",
}

LESSONS["p9-l10-exam"] = {
md: md("Итоговый контроль: альтернативные СУБД и теория", P9, M9B, EX,
    ["Выбрать СУБД под задачу", "Написать запросы MongoDB и Cypher", "Подвести итоги курса"],
    "**Итог курса:** реляционная теория → проектирование → SQL → performance → PostgreSQL internals → admin → DWH → NoSQL/graph/T-SQL/Date.\r\n\r\n**Сценарии выбора СУБД:**\r\n- OLTP university → PostgreSQL\r\n- Analytics grades → DWH star schema\r\n- Flexible catalog → MongoDB or JSONB\r\n- Social/fraud paths → Graph DB\r\n- MS stack shop → T-SQL; cloud neutral → PostgreSQL\r\n\r\nСравнение диалектов T-SQL↔PG, theory Date для критического мышления.",
    [["mongodb", "Главы 1–7 (повторение)"], ["graph-db", "Главы 1–5 (повторение)"], ["date-sql", "Главы 11–14 (повторение)"]],
    [["Polyglot persistence", "разные БД под задачи"], ["Document model", "MongoDB"],
     ["Graph traversal", "Cypher"], ["Relational theory", "Date"]]),

  quiz: quiz("p9-l10-exam",
    sq("q1", "University OLTP best…", ["PostgreSQL ACID", "Mongo only", "Graph only", "No DB"], 0, "OLTP relational."),
    sq("q2", "6-hop friends…", ["Graph DB", "CSV", "pg_hba", "TOAST"], 0, "Traversal workload."),
    sq("q3", "T-SQL TOP → PG…", ["LIMIT", "MERGE", "VACUUM", "RLS"], 0, "Dialect map."),
    sq("q4", "Star schema for grades…", ["DWH analytics", "OLTP only", "WAL", "Auth"], 0, "Dimensional DWH."),
    mq("q5", "Course finale topics? (верные)", ["NoSQL models", "Graph Cypher", "T-SQL vs PG", "Only Part 0"], [0,1,2], "Part 9 recap.")),

  tasks: "## Итоговая аттестация\r\n\r\n1. **Выбор СУБД:** 4 сценария (OLTP, DWH, catalog, social) — обоснуйте выбор.\r\n2. Mongo: find + aggregation ИЛИ псевдокод (без установки).\r\n3. Cypher: MATCH 2-hop path (на бумаге).\r\n4. T-SQL vs PG: 5 пар конструкций.\r\n5. Date: эссе NULL (½ стр.).\r\n6. Рефлексия курса: что изучили, что примените.\r\n7. Все тесты части 9 ≥70%.",
}
for (const [id, content] of Object.entries(LESSONS)) {
  for (const dir of OUT_DIRS) {
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, id + ".md"), content.md.trim() + "\n", "utf8");
    fs.writeFileSync(path.join(dir, id + ".quiz.json"), JSON.stringify(content.quiz, null, 2) + "\n", "utf8");
    fs.writeFileSync(path.join(dir, id + ".tasks.md"), content.tasks.trim() + "\n", "utf8");
  }
  count += 3;
}
console.log("Written " + count + " files (" + Object.keys(LESSONS).length + " lessons)");

# -*- coding: utf-8 -*-
"""Generate enhanced Russian lesson content for Parts 6-9."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIRS = [ROOT / "content" / "lessons", ROOT / "public" / "content" / "lessons"]

def sq(qid, question, options, correct, explanation):
    return {"id": qid, "type": "single", "question": question, "options": options,
            "correct": [correct], "explanation": explanation}

def mq(qid, question, options, correct, explanation):
    return {"id": qid, "type": "multi", "question": question, "options": options,
            "correct": correct, "explanation": explanation}

def quiz(lesson_id, *questions):
    return {"lessonId": lesson_id, "passingScore": 70, "questions": list(questions)}

def md(title, part, mod, dialect_note, objectives, theory, sources, concepts, extra=""):
    obj = "\n".join(f"- {o}" for o in objectives)
    src = "\n".join(f"- **{s[0]}**: {s[1]}" for s in sources)
    con = "\n".join(f"- **{c[0]}** — {c[1]}." for c in concepts)
    return f"""## {title}

**Часть:** {part} · **Модуль:** {mod}

{dialect_note}

### Цели урока

{obj}

### Краткая теория

{theory}

### Что читать в источниках

{src}

### Ключевые понятия

{con}
{extra}"""

def write_lesson(lid, content):
    for d in OUT_DIRS:
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{lid}.md").write_text(content["md"].strip() + "\n", encoding="utf-8")
        (d / f"{lid}.quiz.json").write_text(
            json.dumps(content["quiz"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (d / f"{lid}.tasks.md").write_text(content["tasks"].strip() + "\n", encoding="utf-8")

P6 = "Внутреннее устройство PostgreSQL"
M6 = "Хранение и расширения"
P7 = "Администрирование и архитектуры нагрузок"
M7 = "Безопасность и эксплуатация"
P8 = "Хранилища данных"
M8 = "DWH и dimensional modeling"
P9 = "Альтернативные СУБД и итоговая аттестация"
M9A = "NoSQL и графовые БД"
M9B = "T-SQL, теория Дейта и итог"

THEORY = "theory"
SQL = "Praktika: **PostgreSQL** (psql или pgAdmin)."
TH = "Фокус на теории и тесте; SQL не обязателен."
LAB = "Лaboratornaya. Sreda: **PostgreSQL**."
EX = "Itogovyy test chasti."
CMP = "> **Сравнение диалектов:** T-SQL (SQL Server) ↔ PostgreSQL\n"
OPT = "> **Опционально:** задания можно выполнить на [MongoDB Playground](https://mongoplayground.net) без локальной установки.\n"

LESSONS = {}

# ===== PART 6 =====
LESSONS["p6-l01-storage-arch"] = {
"md": md("Архитектура хранения PostgreSQL", P6, M6, TH,
    ["Описать процессы postmaster и backend", "Объяснить shared buffers и WAL", "Наметить путь запроса к данным"],
    """PostgreSQL — **многопроцессная** СУБД. **Postmaster** принимает подключения и порождает **backend** (один на сессию). Фоновые процессы: checkpointer, walwriter, autovacuum, bgwriter.

**Путь SELECT:** клиент → postmaster → backend → парсер/планировщик → исполнитель → **buffer manager** → страница из **shared_buffers** или с диска (8 КБ).

**Shared buffers** — общий кэш страниц в RAM (`shared_buffers`, обычно ~25% RAM). **Buffer cache hit ratio** = blks_hit / (blks_hit + blks_read) — ключевой KPI.

**WAL** — журнал упреждающей записи: изменения сначала в WAL, потом в data-файлы (durability, crash recovery).

**Оптимизатор** выбирает план по статистике `pg_statistic`: nested loop, hash join, merge join — по оценке cost/rows (см. EXPLAIN).""",
    [("morgunov", "Глава 18, §18.1"), ("novikov", "Глава 13, §13.1")],
    [("Postmaster", "главный процесс кластера"), ("Shared buffers", "кэш страниц данных"),
     ("WAL", "журнал до записи в heap"), ("Backend", "процесс одной сессии")]),
"quiz": quiz("p6-l01-storage-arch",
    sq("q1", "Кто принимает новые подключения?", ["Postmaster", "Walwriter", "Autovacuum", "Checkpointer"], 0, "Postmaster слушает порт."),
    sq("q2", "Shared buffers хранит…", ["Страницы таблиц и индексов", "Только WAL", "pg_hba.conf", "Пароли ролей"], 0, "Основной data cache."),
    sq("q3", "WAL нужен для…", ["Durability и recovery", "Только SELECT", "Создания VIEW", "Шифрования"], 0, "Write-Ahead Log."),
    sq("q4", "Buffer hit ratio растёт когда…", ["Больше чтений из RAM", "Отключён VACUUM", "Нет индексов", "wal_level=minimal"], 0, "blks_hit / (blks_hit+blks_read)."),
    mq("q5", "Фоновые процессы PostgreSQL? (верные)", ["Walwriter", "Checkpointer", "Autovacuum", "MongoDB router"], [0,1,2], "Стандартные фоновые workers.")),
"tasks": """## Задания

1. Нарисуйте схему: клиент → postmaster → backend → shared_buffers → диск.
2. ```sql
   SELECT datname, blks_hit, blks_read,
          round(100.0*blks_hit/nullif(blks_hit+blks_read,0),2) AS hit_pct
   FROM pg_stat_database WHERE datname=current_database();
   ```
3. Объясните связь shared_buffers и latency SELECT.
4. Прочитайте Morgunov §18.1.""",
}

LESSONS["p6-l02-pages-tuples"] = {
"md": md("Страницы, строки и HOT-обновления", P6, M6, TH,
    ["Описать структуру heap page", "Объяснить HOT и index-only scan", "Связать физику с производительностью"],
    """**Heap page** (8 КБ): заголовок, line pointers, **tuple** (строки). Tuple содержит xmin/xmax (MVCC) и данные.

**UPDATE** создаёт новую версию tuple; старая — **dead tuple** → нужен VACUUM.

**HOT (Heap-Only Tuple):** UPDATE без изменения индексированных столбцов, новая версия на той же странице — индексы не трогаем.

**Index-Only Scan:** все столбцы в индексе + **visibility map** подтверждает видимость — heap не читается.

**Алгоритмы JOIN:**

| Алгоритм | Условие | I/O |
|----------|---------|-----|
| Nested Loop | Малая таблица + индекс | Random |
| Hash Join | Равенство, влезает в work_mem | Seq + hash |
| Merge Join | Отсортированные входы | Sequential |

**FILLFACTOR 80** оставляет место для HOT на часто обновляемых таблицах (`performance`).""",
    [("morgunov", "Глава 18, §18.2"), ("komarov", "Раздел 11: физическое хранение")],
    [("Heap page", "8 КБ страница данных"), ("HOT", "update без обновления индексов"),
     ("Dead tuple", "устаревшая версия строки"), ("Visibility map", "карта видимых страниц")]),
"quiz": quiz("p6-l02-pages-tuples",
    sq("q1", "Размер страницы по умолчанию?", ["8 КБ", "4 КБ", "16 КБ", "1 КБ"], 0, "BLCKSZ=8192."),
    sq("q2", "HOT возможен когда…", ["Не меняются индексированные столбцы", "Меняется PK", "Нет WAL", "Только DELETE"], 0, "Условия HOT."),
    sq("q3", "Hash Join выгоден при…", ["Equi-join и достаточно work_mem", "CROSS JOIN", "Нет статистики", "Только OUTER JOIN"], 0, "Hash по ключу равенства."),
    sq("q4", "Dead tuples появляются после…", ["UPDATE и DELETE", "SELECT", "CREATE INDEX", "GRANT"], 0, "MVCC версионирование."),
    mq("q5", "Index-Only Scan требует… (верные)", ["Covering index", "Актуальную visibility map", "CROSS JOIN", "Все столбцы в индексе"], [0,1,3], "Heap может не читаться.")),
"tasks": """## Задания

1. Опишите структуру heap page.
2. EXPLAIN (ANALYZE, BUFFERS) для JOIN student + performance — укажите тип join.
3. Когда задать FILLFACTOR 70 для `performance`?
4. Связь dead tuples и autovacuum.""",
}

LESSONS["p6-l03-wal"] = {
"md": md("Write-Ahead Log и контрольные точки", P6, M6, TH,
    ["Объяснить назначение WAL", "Настроить checkpoint и wal_level", "Понять crash recovery"],
    """**WAL:** сначала запись в журнал, затем в data-файлы. COMMIT подтверждается после fsync WAL.

Сегменты в `pg_wal/` (~16 МБ). **Checkpoint** сбрасывает dirty buffers, позволяет recycle WAL. Параметры: `checkpoint_timeout`, `max_wal_size`, `checkpoint_completion_target`.

**Crash recovery:** redo WAL с последнего checkpoint; незавершённые TX — rollback.

| wal_level | Применение |
|-----------|------------|
| minimal | Только recovery |
| replica | Streaming replication, base backup |
| logical | Logical replication |

WAL — основа **репликации** и **PITR** (point-in-time recovery).""",
    [("morgunov", "Глава 18, §18.3"), ("novikov", "Глава 13, §13.2")],
    [("WAL", "журнал упреждающей записи"), ("Checkpoint", "точка сброса на диск"),
     ("LSN", "Log Sequence Number"), ("Redo", "повтор изменений при recovery")]),
"quiz": quiz("p6-l03-wal",
    sq("q1", "Правило WAL?", ["Сначала WAL, потом data", "Сначала data", "WAL только чтение", "WAL=индекс"], 0, "Write-Ahead."),
    sq("q2", "wal_level=replica для…", ["Физической репликации", "Только VACUUM", "Отключения журнала", "MongoDB"], 0, "Streaming replication."),
    sq("q3", "Checkpoint…", ["Сбрасывает dirty pages", "Удаляет таблицы", "Создаёт роли", "Строит GIN"], 0, "Checkpointer process."),
    sq("q4", "При аварийном restart…", ["Replay WAL", "Пустая БД", "Только pg_dump", "Drop database"], 0, "Crash recovery."),
    mq("q5", "Параметры checkpoint? (верные)", ["max_wal_size", "checkpoint_timeout", "checkpoint_completion_target", "MongoDB port"], [0,1,2], "Настройка частоты CP.")),
"tasks": """## Задания

1. Запишите wal_level, max_wal_size, checkpoint_timeout.
2. `SELECT pg_current_wal_lsn(), pg_walfile_name(pg_current_wal_lsn());`
3. Timeline: COMMIT → WAL → checkpoint → data files.
4. Разница minimal vs replica vs logical.""",
}

LESSONS["p6-l04-tablespaces"] = {
"md": md("Tablespaces и размещение данных", P6, M6, SQL,
    ["Создать tablespace на отдельном диске", "Перенести индексы и таблицы", "Спланировать I/O нагрузку"],
    """**Tablespace** — имя → путь на диске. По умолчанию: `pg_default`, `pg_global`.

Зачем: разделение I/O (SSD для индексов OLTP, HDD для архива), обслуживание без переустановки.

```sql
CREATE TABLESPACE fast_ssd LOCATION '/mnt/ssd/pgdata';
CREATE INDEX idx ON performance(student_id) TABLESPACE fast_ssd;
ALTER TABLE archive_log SET TABLESPACE slow_hdd;
```

План: `student`, `performance` — быстрый диск; архив оценок — медленный.""",
    [("morgunov", "Глава 19, §19.1"), ("komarov", "Раздел 12: tablespaces")],
    [("Tablespace", "логическое размещение файлов"), ("pg_tablespace", "системный каталог"),
     ("I/O planning", "распределение по дискам")]),
"quiz": quiz("p6-l04-tablespaces",
    sq("q1", "Tablespace — это…", ["Путь хранения файлов БД", "SQL-схема", "Тип JOIN", "WAL-сегмент"], 0, "Физическое размещение."),
    sq("q2", "CREATE INDEX ... TABLESPACE t1…", ["Кладёт файлы индекса в t1", "Создаёт VIEW", "Включает RLS", "Drop table"], 0, "Индексы тоже в tablespace."),
    sq("q3", "SSD для индексов OLTP…", ["Снижает random read latency", "Отключает WAL", "Заменяет VACUUM", "Только для TOAST"], 0, "Random I/O на SSD быстрее."),
    sq("q4", "DROP TABLESPACE требует…", ["Пустой tablespace", "pg_dump", "REINDEX ALL", "wal_level logical"], 0, "Все объекты перенесены."),
    mq("q5", "Сценарии tablespace? (верные)", ["Hot data SSD", "Archive HDD", "Разделение индексов", "Замена SQL"], [0,1,2], "Физическое tiering.")),
"tasks": """## Практика PostgreSQL

1. `SELECT spcname, pg_tablespace_location(oid) FROM pg_tablespace;`
2. Создайте tablespace (если есть каталог) и таблицу test_ts.
3. Опишите размещение student vs performance_archive.
4. Сохраните: `course/sql/p6-l04-tablespaces-solution.sql`""",
}

LESSONS["p6-l05-toast"] = {
"md": md("TOAST и хранение больших значений", P6, M6, TH,
    ["Объяснить механизм TOAST", "Выбрать стратегию storage для JSON/BLOB", "Диагностировать раздувание строк"],
    """**TOAST** — хранение значений > ~2 КБ вне основной страницы.

| STORAGE | Поведение |
|---------|-----------|
| EXTENDED | Сжатие + out-of-line (default text/json) |
| EXTERNAL | Out-of-line без сжатия |
| MAIN | Сжатие, out-of-line если не влезает |
| PLAIN | Без TOAST |

Большие JSON хранятся в **TOAST-таблице**; heap tuple — указатель. `pg_column_size(row)` — полный размер.

Рекомендации: не тащить BLOB в hot OLTP-row; GIN по нужным ключам JSON; редко обновляемые большие поля — в отдельную 1:1 таблицу.""",
    [("morgunov", "Глава 19, §19.2"), ("novikov", "Глава 13, §13.3")],
    [("TOAST", "oversized attribute storage"), ("Out-of-line", "данные вне heap page"),
     ("pg_column_size", "размер строки с TOAST")]),
"quiz": quiz("p6-l05-toast",
    sq("q1", "TOAST активируется…", ["При больших значениях столбца", "При CREATE USER", "При JOIN", "При RLS"], 0, "Oversized attributes."),
    sq("q2", "EXTENDED стратегия…", ["Сжимает и выносит", "Запрещает NULL", "Создаёт BRIN", "WAL off"], 0, "Default для text."),
    sq("q3", "TOAST-данные лежат…", ["В отдельной TOAST-таблице", "В pg_hba", "В shared_buffers only", "В MongoDB"], 0, "Out-of-line storage."),
    sq("q4", "pg_column_size показывает…", ["Размер с TOAST", "Только PK", "Plan cost", "LSN"], 0, "Включая out-of-line."),
    mq("q5", "OLTP с большим JSON? (верные)", ["GIN по ключам", "Отдельная таблица", "Редкий UPDATE blob", "CROSS JOIN всего"], [0,1,2], "Минимизировать hot row width.")),
"tasks": """## Задания

1. Таблица с text >100KB → pg_column_size().
2. EXTENDED vs EXTERNAL — когда EXTERNAL?
3. TOAST в схеме университета (описания курсов)?
4. Связь TOAST-bloat и VACUUM.""",
}

LESSONS["p6-l06-extensions"] = {
"md": md("Расширения PostgreSQL: установка и обзор", P6, M6, SQL,
    ["Установить расширение через CREATE EXTENSION", "Использовать pg_trgm и uuid-ossp", "Оценить совместимость версий"],
    """**Extensions** — упакованные модули: типы, функции, операторы, FDW.

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

**pg_trgm** — триграммы для LIKE/ similarity, GIN/GiST индексы нечёткого поиска.

**uuid-ossp** — генерация UUID (`uuid_generate_v4()`).

**pg_stat_statements** — топ SQL по времени/вызовам (нужен shared_preload_libraries).

**Полнотекстовый поиск:**
```sql
CREATE EXTENSION pg_trgm; -- fuzzy
-- tsvector/tsquery (встроено):
SELECT to_tsvector('russian', 'база данных') @@ to_tsquery('russian', 'база');
CREATE INDEX idx_fts ON docs USING GIN (to_tsvector('russian', body));
```

Совместимость: `SELECT * FROM pg_available_extensions;` — версия extension vs server.""",
    [("morgunov", "Глава 20, §20.1"), ("komarov", "Раздел 13: extensions")],
    [("CREATE EXTENSION", "установка модуля"), ("pg_trgm", "триграммный поиск"),
     ("tsvector", "лексемы полнотекстового поиска"), ("pg_stat_statements", "статистика SQL")]),
"quiz": quiz("p6-l06-extensions",
    sq("q1", "CREATE EXTENSION…", ["Устанавливает модуль в БД", "Создаёт tablespace", "Drop WAL", "MongoDB sync"], 0, "Регистрация extension."),
    sq("q2", "pg_trgm для…", ["Нечёткого текстового поиска", "Replication", "Backup", "RLS"], 0, "Trigram similarity."),
    sq("q3", "GIN + to_tsvector…", ["Полнотекстовый индекс", "Hash join", "TOAST only", "Seq scan only"], 0, "FTS index."),
    sq("q4", "pg_stat_statements требует…", ["shared_preload_libraries", "wal_level minimal", "No indexes", "MongoDB"], 0, "Preload at startup."),
    mq("q5", "Популярные extensions? (верные)", ["pg_trgm", "uuid-ossp", "pg_stat_statements", "Cypher"], [0,1,2], "Стандартный набор DBA.")),
"tasks": """## Практика PostgreSQL

1. `SELECT name, default_version FROM pg_available_extensions ORDER BY name LIMIT 20;`
2. CREATE EXTENSION pg_trgm; — similarity('student','students').
3. FTS: to_tsvector/to_tsquery по русскому тексту.
4. Сохраните: `course/sql/p6-l06-extensions-solution.sql`""",
}

LESSONS["p6-l07-monitoring-ext"] = {
"md": md("Мониторинг: pg_stat и pg_stat_statements", P6, M6, SQL,
    ["Читать pg_stat_activity и pg_locks", "Найти долгие запросы", "Настроить pg_stat_statements"],
    """**pg_stat_activity** — активные сессии: state, query, wait_event, duration.

```sql
SELECT pid, usename, state, now()-query_start AS dur, left(query,80)
FROM pg_stat_activity WHERE state <> 'idle' ORDER BY dur DESC;
```

**pg_locks** — блокировки; join с activity для диагностики deadlocks.

**pg_stat_user_tables** — seq_scan vs idx_scan, n_live_tup, last_autovacuum.

**pg_stat_statements** (extension):
```sql
SELECT calls, mean_exec_time, rows, left(query,100)
FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;
```

**Оптимизатор:** если seq_scan доминирует — нужны индексы; высокий mean_time — EXPLAIN ANALYZE, переписать JOIN, обновить статистику `ANALYZE`.

**Buffer monitoring:** `pg_stat_bgwriter`, `pg_buffercache` (extension).""",
    [("morgunov", "Глава 20, §20.2"), ("novikov", "Глава 14, §14.1")],
    [("pg_stat_activity", "активные сессии"), ("pg_locks", "блокировки"),
     ("pg_stat_statements", "агрегат по SQL"), ("wait_event", "ожидание I/O/lock")]),
"quiz": quiz("p6-l07-monitoring-ext",
    sq("q1", "Долгий запрос ищем в…", ["pg_stat_activity", "pg_hba.conf", "TOAST", "MongoDB"], 0, "query_start, state."),
    sq("q2", "pg_stat_statements показывает…", ["Топ SQL по времени", "Только DDL", "Только roles", "WAL size"], 0, "Aggregate query stats."),
    sq("q3", "seq_scan >> idx_scan означает…", ["Возможно нужны индексы", "Всё оптимально", "WAL broken", "RLS off"], 0, "Missing indexes hint."),
    sq("q4", "pg_locks + activity для…", ["Диагностики блокировок", "Backup", "FTS", "TOAST"], 0, "Lock troubleshooting."),
    mq("q5", "Действия при медленном query? (верные)", ["EXPLAIN ANALYZE", "ANALYZE table", "Проверить индексы", "Игнорировать"], [0,1,2], "Стандартный tuning flow.")),
"tasks": """## Практика PostgreSQL

1. pg_stat_activity — найдите самый долгий active query.
2. pg_stat_user_tables — seq_scan vs idx_scan для performance.
3. Установите pg_stat_statements, top-5 по total_time.
4. EXPLAIN ANALYZE медленного JOIN — предложите индекс.""",
}

LESSONS["p6-l08-exam"] = {
"md": md("Контроль: хранение и расширения PostgreSQL", P6, M6, EX,
    ["Объяснить путь записи на диск", "Спланировать tablespace", "Подключить расширение для задачи"],
    """Итоговый контроль части 6. Темы: архитектура процессов, страницы/MVCC/HOT, WAL/checkpoint, tablespaces, TOAST, extensions (pg_trgm, FTS), мониторинг pg_stat*.

**Ключевые связи:** WAL → recovery/replication; shared_buffers → hit ratio; HOT/FILLFACTOR → UPDATE performance; pg_stat_statements → tuning; GIN+tsvector → полнотекстовый поиск.""",
    [("morgunov", "Главы 18–20 (повторение)"), ("novikov", "Главы 13–14 (повторение)")],
    [("Buffer pool", "shared_buffers"), ("WAL", "durability"), ("HOT", "update optimization"),
     ("Extensions", "модули PostgreSQL")]),
"quiz": quiz("p6-l08-exam",
    sq("q1", "COMMIT гарантирует durability через…", ["WAL fsync", "Только shared_buffers", "TOAST", "pg_trgm"], 0, "WAL persistence."),
    sq("q2", "HOT снижает…", ["Нагрузку на индексы при UPDATE", "Размер WAL", "Need for SELECT", "Replication lag always"], 0, "Index updates skipped."),
    sq("q3", "Tablespace позволяет…", ["Разнести I/O по дискам", "Заменить JOIN", "Отключить MVCC", "MongoDB embed"], 0, "Physical placement."),
    sq("q4", "pg_stat_statements для…", ["Поиска тяжёлых запросов", "RLS policies", "TDE", "Graph traversal"], 0, "Query performance stats."),
    mq("q5", "Часть 6 охватывает? (верные)", ["Storage pages", "WAL", "Extensions/FTS", "Cypher only"], [0,1,2], "PostgreSQL internals.")),
"tasks": """## Итоговая работа

1. Повторите уроки p6-l01 … p6-l07.
2. Напишите эссе (1 стр.): путь INSERT от backend до диска через WAL.
3. Схема tablespace для OLTP университета.
4. Список 3 extensions для мониторинга + FTS + UUID.
5. Пройдите все тесты части 6 (≥70%).""",
}

# Continue in part 2 - load from external or append
exec(open(Path(__file__).parent / "enhance_p6_p9_part2.py", encoding="utf-8").read())

def main():
    count = 0
    for lid, content in LESSONS.items():
        write_lesson(lid, content)
        count += 3
    print(f"Written {count} files ({len(LESSONS)} lessons)")

if __name__ == "__main__":
    main()

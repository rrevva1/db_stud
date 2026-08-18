## Архитектура хранения PostgreSQL

**Часть:** Внутреннее устройство PostgreSQL · **Модуль:** Хранение и расширения

Фокус на теории и тесте; SQL не обязателен.

### Цели урока

- Описать процессы postmaster и backend
- Объяснить shared buffers и WAL
- Наметить путь запроса к данным

### Краткая теория

PostgreSQL — **многопроцессная** СУБД. **Postmaster** принимает подключения и порождает **backend** (один на сессию). Фоновые процессы: checkpointer, walwriter, autovacuum, bgwriter.

**Путь SELECT:** клиент → postmaster → backend → парсер/планировщик → исполнитель → **buffer manager** → страница из **shared_buffers** или с диска (8 КБ).

**Shared buffers** — общий кэш страниц в RAM (`shared_buffers`, обычно ~25% RAM). **Buffer cache hit ratio** = blks_hit / (blks_hit + blks_read) — ключевой KPI.

**WAL** — журнал упреждающей записи: изменения сначала в WAL, потом в data-файлы (durability, crash recovery).

**Оптимизатор** выбирает план по статистике `pg_statistic`: nested loop, hash join, merge join — по оценке cost/rows (см. EXPLAIN).

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 18, §18.1
2. **2-я очередь.** Новиков Б. А. и др. — Основы технологий баз данных — Глава 13, §13.1
### Ключевые понятия

- **Postmaster** — главный процесс кластера.
- **Shared buffers** — кэш страниц данных.
- **WAL** — журнал до записи в heap.
- **Backend** — процесс одной сессии.

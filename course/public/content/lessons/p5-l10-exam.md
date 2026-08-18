## Контроль: индексы, оптимизация и динамический SQL

**Часть:** Производительность и оптимизация · **Модуль:** Обслуживание и динамический SQL

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Подобрать индексы для рабочей нагрузки
- Проанализировать план запроса
- Написать безопасный динамический SQL

### Краткая теория

Итоговый контроль части 5 охватывает:

1. **Индексы** — B-tree, составные, partial, INCLUDE, GIN/GiST/BRIN.
2. **EXPLAIN ANALYZE** — чтение плана, Seq vs Index Scan, joins.
3. **Оптимизация** — ANALYZE, рефакторинг SQL, pg_stat_statements.
4. **Секционирование** — RANGE/LIST/HASH, partition pruning.
5. **VACUUM** — MVCC, dead tuples, autovacuum.
6. **Динамический SQL** — EXECUTE, format, защита от injection.

#### Чеклист DBA/разработчика

| Шаг | Действие |
|-----|----------|
| 1 | EXPLAIN (ANALYZE, BUFFERS) медленного запроса |
| 2 | Проверить estimated vs actual rows |
| 3 | ANALYZE / индекс / переписать SQL |
| 4 | Мониторинг n_dead_tup, autovacuum |
| 5 | Dynamic SQL — whitelist + USING |

#### Связанные SQL-лабы

- `course/sql/p5-l01-indexes-btree.sql`
- `course/sql/p5-l03-explain-analyze.sql`
- `course/sql/p5-l04-transactions-acid.sql`
- `course/sql/p5-l06-functions-plpgsql.sql`

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Главы 14–17 (повторение)
2. **2-я очередь.** Edward Pollack — Dynamic SQL (2nd ed.) — Главы 1–6 (повторение)
### Ключевые понятия

Повторите материал уроков p5-l01 … p5-l09.

Сквозная предметная область: **университет**, **авиакомпания**.

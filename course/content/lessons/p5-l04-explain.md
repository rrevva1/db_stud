## EXPLAIN и EXPLAIN ANALYZE

**Часть:** Производительность и оптимизация · **Модуль:** Индексы и планы выполнения

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Читать план запроса PostgreSQL
- Найти Seq Scan и Nested Loop
- Интерпретировать cost и actual time

### Краткая теория

**EXPLAIN** показывает **план выполнения** — как оптимизатор намерен получить данные. **EXPLAIN ANALYZE** выполняет запрос и добавляет **фактические** времена и число строк.

```sql
EXPLAIN SELECT * FROM employee WHERE id = 1;

EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM employee e
JOIN department d ON d.id = e.department_id
WHERE e.salary > 50000;
```

#### Основные узлы плана

| Узел | Смысл |
|------|--------|
| Seq Scan | Полное сканирование таблицы |
| Index Scan | Обход B-tree + чтение heap |
| Index Only Scan | Только индекс (covering) |
| Bitmap Index Scan + Bitmap Heap Scan | Комбинация для нескольких условий |
| Nested Loop | Для каждой строки слева — поиск справа |
| Hash Join | Построение hash-таблицы на меньшей стороне |
| Merge Join | Слияние отсортированных потоков |
| Sort / HashAggregate | Сортировка / агрегация через hash |

#### cost и rows

```
Index Scan ...  (cost=0.29..8.30 rows=1 width=...)
```

- **cost** — условные единицы (startup..total), не миллисекунды
- **rows** — оценка планировщика (может ошибаться без ANALYZE)

#### EXPLAIN ANALYZE

```
Index Scan ... (actual time=0.020..0.021 rows=1 loops=1)
```

- **actual time** — реальное время (ms) startup..total
- **rows** — фактически прочитано
- **loops** — сколько раз узел вызывался (важно в Nested Loop)

#### BUFFERS

`shared hit` — из cache; `read` — с диска. Много read → возможно, не хватает shared_buffers.

#### Типичные проблемы

1. **Seq Scan на большой таблице** — нет индекса или низкая селективность
2. **Nested Loop с большим loops** — не тот join order
3. **rows estimate сильно ≠ actual** — устаревшая статистика → `ANALYZE`
4. **Sort на огромном наборе** — нужен индекс для ORDER BY или больше work_mem

#### Настройки для отладки

```sql
SET enable_seqscan = off;  -- только для теста!
SET max_parallel_workers_per_gather = 4;
```

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 15, §15.1
2. **2-я очередь.** Elizabeth Noble — Pro T-SQL 2019 — Глава 10: планы выполнения
### Ключевые понятия

- EXPLAIN vs EXPLAIN ANALYZE
- Seq Scan, Index Scan, Join types
- cost, rows, actual time, BUFFERS

См. также: `course/sql/p5-l03-explain-analyze.sql`

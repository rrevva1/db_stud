## B-tree, Hash и составные индексы

**Часть:** Производительность и оптимизация · **Модуль:** Индексы и планы выполнения

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Выбрать тип индекса для запроса
- Построить составной индекс
- Использовать INCLUDE и partial index

### Краткая теория

#### B-tree (универсальный)

Подходит для большинства сравнений и сортировки. **Составной индекс** `(a, b, c)` поддерживает поиск по префиксу:

- `(a)`, `(a,b)`, `(a,b,c)` — да
- только `(b)` или `(c)` — обычно нет (исключение: index skip scan в других СУБД; в PG — нет)

```sql
CREATE INDEX idx_orders_cust_date ON orders (customer_id, order_date DESC);
```

Порядок столбцов важен: сначала высокоселективный или равенство в WHERE, затем диапазон.

#### Hash

```sql
CREATE INDEX idx_hash_email ON users USING hash (email);
```

Только **равенство** `=`. После PG 10 hash индексы WAL-safe. Редко нужен — B-tree часто достаточно.

#### INCLUDE (covering index)

```sql
CREATE INDEX idx_cover ON orders (customer_id) INCLUDE (total_amount, status);
```

Index-Only Scan: ключ в индексе + включённые столбцы без обращения к heap (при видимости VM).

#### Partial index (частичный)

```sql
CREATE INDEX idx_active ON employee (department_id)
WHERE fired_at IS NULL;
```

Меньше размер, быстрее — только для подмножества строк, matching WHERE в запросе.

#### UNIQUE и составной ключ

```sql
CREATE UNIQUE INDEX idx_enrollment ON enrollment (student_id, course_id);
```

#### Выбор типа

| Сценарий | Индекс |
|----------|--------|
| =, <, >, сортировка | B-tree |
| Только = на огромной таблице (редко) | Hash |
| JSON, массивы, fulltext | GIN (след. урок) |
| Очень большая таблица, корреляция с физ. порядком | BRIN |

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 14, §14.2
2. **2-я очередь.** Комаров В. И. — Путеводитель по базам данных — Раздел 8: индексы
### Ключевые понятия

- Составной индекс, левый префикс
- INCLUDE, partial index
- Index-Only Scan

Сквозная предметная область: **университет**, **авиакомпания**.

## Секционирование таблиц

**Часть:** Производительность и оптимизация · **Модуль:** Обслуживание и динамический SQL

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Создать RANGE и LIST секции
- Настроить секционирование по HASH
- Выполнить partition pruning

### Краткая теория

**Секционирование (partitioning)** делит одну логическую таблицу на **физические части** (partition). Запросы с фильтром по ключу секционирования могут читать только нужные части — **partition pruning**.

#### Декларативное секционирование (PG 10+)

```sql
CREATE TABLE measurement (
    city_id   INT NOT NULL,
    log_date  DATE NOT NULL,
    peaktemp  INT,
    unitsales INT
) PARTITION BY RANGE (log_date);

CREATE TABLE measurement_y2024m01
    PARTITION OF measurement
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE measurement_y2024m02
    PARTITION OF measurement
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
```

#### LIST

```sql
CREATE TABLE sales (region text, amount numeric)
PARTITION BY LIST (region);

CREATE TABLE sales_eu PARTITION OF sales FOR VALUES IN ('DE','FR','IT');
CREATE TABLE sales_us PARTITION OF sales FOR VALUES IN ('US','CA');
```

#### HASH

```sql
CREATE TABLE events (id bigint, payload jsonb)
PARTITION BY HASH (id);

CREATE TABLE events_p0 PARTITION OF events FOR VALUES WITH (MODULUS 4, REMAINDER 0);
-- ... p1, p2, p3
```

#### Partition pruning

```sql
EXPLAIN SELECT * FROM measurement WHERE log_date = '2024-01-15';
-- только measurement_y2024m01, не все секции
```

Pruning работает для констант и параметров (зависит от версии и plan cache).

#### Индексы

Индекс создаётся **на каждой секции** или через `CREATE INDEX ON ONLY parent` + attach (PG 11+).

#### Когда секционировать

- Очень большие таблицы (time series, логи)
- Архивация: DROP старой секции вместо DELETE
- Разная политика хранения по регионам

Не секционируйте «на будущее» маленькие таблицы — overhead на планирование.

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 16, §16.1
2. **2-я очередь.** Новиков Б. А. и др. — Основы технологий баз данных — Глава 12, §12.2
### Ключевые понятия

- RANGE, LIST, HASH partitioning
- Partition pruning
- Управление жизненным циклом секций

См. также: `course/sql/p5-l06-functions-plpgsql.sql` (функции для управления секциями)

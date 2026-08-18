## ETL и ELT: загрузка данных в DWH

**Часть:** Хранилища данных · **Модуль:** DWH и dimensional modeling

Фокус на теории и тесте; SQL не обязателен.

### Цели урока

- Описать этапы extract, transform, load
- Сравнить ETL и ELT
- Спроектировать staging area

### Краткая теория

**ETL:** Extract (OLTP, APIs) → Transform (cleanse, conform, surrogate keys) → Load (fact/dim).

**ELT:** Extract → Load raw to staging (cloud DWH) → Transform in SQL (BigQuery, Snowflake).

**Staging area:** копии source tables; validation; audit columns (load_date, batch_id).

**Steps для university DWH:**
1. Extract student, performance из PostgreSQL OLTP.
2. Transform: lookup surrogate keys, handle SCD Type 2 для student.
3. Load fact_grade, refresh dim_*.

**Quality:** dedup, null checks, FK integrity, reconciliation counts.

**Tools:** pg_dump/COPY, Apache Airflow, dbt, custom Python/SQL scripts.

Smirnov: медленно меняющиеся измерения, late arriving facts, incremental load.

### Что читать в источниках

1. **1-я очередь.** Дзгоев А. Э. — Проектирование и разработка баз и хранилищ данных. Лекция 1 — Слайды 111–120
2. **2-я очередь.** Смирнов М. В. — Проектирование хранилищ данных — Глава 5
### Ключевые понятия

- **ETL** — extract-transform-load.
- **Staging** — промежуточная область.
- **Incremental load** — дельта-загрузка.
- **dbt** — transform in warehouse.

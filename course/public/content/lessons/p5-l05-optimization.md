## Оптимизация запросов и статистика

**Часть:** Производительность и оптимизация · **Модуль:** Индексы и планы выполнения

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Обновить статистику командой ANALYZE
- Переписать запрос для лучшего плана
- Применить pg_stat_statements

### Краткая теория

Оптимизатор PostgreSQL использует **статистику** (гistograms, ndistinct, correlation) из `pg_statistic`. Без актуальной статистики — плохие оценки rows → неверный план.

#### ANALYZE

```sql
ANALYZE employee;
ANALYZE VERBOSE employee (salary, department_id);
```

Autovacuum запускает ANALYZE автоматически; после массовой загрузки — ручной `ANALYZE`.

#### Переписывание запросов

**1. Избегайте функций на индексируемых столбцах:**

```sql
-- плохо
WHERE date(created_at) = '2024-01-01'
-- лучше
WHERE created_at >= '2024-01-01' AND created_at < '2024-01-02'
```

**2. EXISTS вместо IN с большим подзапросом** — часто эффективнее и безопаснее с NULL.

**3. JOIN вместо коррелированного подзапроса** в SELECT.

**4. Фильтр раньше** — уменьшайте набор в CTE/подзапросе до JOIN.

**5. LIMIT без ORDER BY** — дешёво; с ORDER BY — нужен индекс или sort.

#### pg_stat_statements

Расширение для топа тяжёлых запросов:

```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

SELECT
    calls,
    mean_exec_time,
    total_exec_time,
    query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

Требует `shared_preload_libraries = 'pg_stat_statements'` в postgresql.conf.

#### Другие инструменты

- `EXPLAIN (ANALYZE, BUFFERS)` — точечная диагностика
- `pg_stat_user_tables` — seq_scan vs idx_scan
- `auto_explain` — лог медленных планов

#### work_mem и параллелизм

Большие Sort/Hash могут использовать disk temp files при малом `work_mem`. Parallel Seq Scan ускоряет большие scan на многоядерных CPU.

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 15, §15.2
2. **2-я очередь.** Комаров В. И. — Путеводитель по базам данных — Раздел 9: оптимизация
### Ключевые понятия

- ANALYZE, статистика планировщика
- Рефакторинг SQL
- pg_stat_statements, мониторинг

Сквозная предметная область: **университет**, **авиакомпания**.

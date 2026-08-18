## Мониторинг: pg_stat и pg_stat_statements

**Часть:** Внутреннее устройство PostgreSQL · **Модуль:** Хранение и расширения

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Читать pg_stat_activity и pg_locks
- Найти долгие запросы
- Настроить pg_stat_statements

### Краткая теория

**pg_stat_activity** — активные сессии: state, query, wait_event, duration.

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

**Buffer monitoring:** `pg_stat_bgwriter`, `pg_buffercache` (extension).

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 20, §20.2
2. **2-я очередь.** Новиков Б. А. и др. — Основы технологий баз данных — Глава 14, §14.1
### Ключевые понятия

- **pg_stat_activity** — активные сессии.
- **pg_locks** — блокировки.
- **pg_stat_statements** — агрегат по SQL.
- **wait_event** — ожидание I/O/lock.

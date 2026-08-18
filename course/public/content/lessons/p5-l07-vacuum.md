## VACUUM, AUTOVACUUM и bloat

**Часть:** Производительность и оптимизация · **Модуль:** Обслуживание и динамический SQL

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Запустить VACUUM и VACUUM FULL
- Объяснить MVCC и dead tuples
- Настроить autovacuum

### Краткая теория

PostgreSQL использует **MVCC** (Multi-Version Concurrency Control): `UPDATE` не перезаписывает строку на месте — создаёт новую версию; старая становится **dead tuple**, видимой только старым снимкам.

#### Dead tuples и bloat

Мёртвые версии занимают место до **VACUUM**. Накопление → **bloat** (раздувание таблицы), замедление seq scan, лишний I/O.

```sql
SELECT relname, n_live_tup, n_dead_tup, last_vacuum, last_autovacuum
FROM pg_stat_user_tables
WHERE schemaname = 'public';
```

#### VACUUM

```sql
VACUUM employee;
VACUUM (VERBOSE, ANALYZE) employee;
```

- Помечает dead tuples как переиспользуемые
- **Не** возвращает место ОС (кроме краев truncate-like случаев)
- Обновляет visibility map для Index-Only Scan
- Может запускаться параллельно с обычными операциями

#### VACUUM FULL

```sql
VACUUM FULL employee;
```

Переписывает таблицу компактно — **возвращает место диску**, но **эксклюзивная блокировка** и медленно. В production предпочитают `pg_repack` или секционирование + DROP.

#### Autovacuum

Фоновый процесс по порогам:

```
autovacuum_vacuum_threshold + autovacuum_vacuum_scale_factor * n_live
```

Настройки per-table:

```sql
ALTER TABLE big_log SET (
    autovacuum_vacuum_scale_factor = 0.01,
    autovacuum_analyze_scale_factor = 0.005
);
```

#### Freeze и transaction id wraparound

VACUUM **freezes** старые xmin — критично для предотвращения wraparound. Следите за `age(relfrozenxid)` в `pg_class`.

#### ANALYZE vs VACUUM

| Команда | Назначение |
|---------|------------|
| VACUUM | Dead tuples, freeze, visibility map |
| ANALYZE | Статистика для планировщика |
| VACUUM ANALYZE | Оба |

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 16, §16.2
2. **2-я очередь.** Комаров В. И. — Путеводитель по базам данных — Раздел 10: обслуживание
### Ключевые понятия

- MVCC, dead tuple, bloat
- VACUUM, VACUUM FULL, autovacuum
- Freeze, transaction id

Сквозная предметная область: **университет**, **авиакомпания** (таблицы с частыми UPDATE).

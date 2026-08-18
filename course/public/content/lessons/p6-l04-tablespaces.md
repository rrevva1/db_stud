## Tablespaces и размещение данных

**Часть:** Внутреннее устройство PostgreSQL · **Модуль:** Хранение и расширения

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Создать tablespace на отдельном диске
- Перенести индексы и таблицы
- Спланировать I/O нагрузку

### Краткая теория

**Tablespace** — имя → путь на диске. По умолчанию: `pg_default`, `pg_global`.

Зачем: разделение I/O (SSD для индексов OLTP, HDD для архива), обслуживание без переустановки.

```sql
CREATE TABLESPACE fast_ssd LOCATION '/mnt/ssd/pgdata';
CREATE INDEX idx ON performance(student_id) TABLESPACE fast_ssd;
ALTER TABLE archive_log SET TABLESPACE slow_hdd;
```

План: `student`, `performance` — быстрый диск; архив оценок — медленный.

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 19, §19.1
2. **2-я очередь.** Комаров В. И. — Путеводитель по базам данных — Раздел 12: tablespaces
### Ключевые понятия

- **Tablespace** — логическое размещение файлов.
- **pg_tablespace** — системный каталог.
- **I/O planning** — распределение по дискам.

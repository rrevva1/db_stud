## Резервное копирование: pg_dump и pg_basebackup

**Часть:** Администрирование и архитектуры нагрузок · **Модуль:** Безопасность и эксплуатация

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Сделать логический дамп pg_dump
- Выполнить физический base backup
- Восстановить БД из резервной копии

### Краткая теория

**Логический backup — pg_dump:**
```bash
pg_dump -Fc -f university.dump university_db
pg_restore -d university_new university.dump
```
Портативный, выборочный; медленнее на huge DB.

**Физический — pg_basebackup:**
```bash
pg_basebackup -D /backup/base -Ft -z -P
```
Копия data directory + WAL для PITR. Требует wal_level=replica, replication slot.

**PITR:** archive_mode + restore_command → recovery до точки во времени.

**Стратегия:** RPO/RTO; ежедневный dump + continuous WAL archive; тест restore регулярно.

**pg_dump --schema-only** для DDL; **--data-only** для данных.

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 22, §22.1
2. **2-я очередь.** Душан Петкович — Microsoft SQL Server 2012. Руководство для начинающих — Глава 10: backup
### Ключевые понятия

- **pg_dump** — логический дамп.
- **pg_basebackup** — физическая копия.
- **PITR** — восстановление на момент времени.
- **RPO/RTO** — допустимая потеря/простой.

## Контроль: хранение и расширения PostgreSQL

**Часть:** Внутреннее устройство PostgreSQL · **Модуль:** Хранение и расширения

Итоговый тест части.

### Цели урока

- Объяснить путь записи на диск
- Спланировать tablespace
- Подключить расширение для задачи

### Краткая теория

Итоговый контроль части 6. Темы: архитектура процессов, страницы/MVCC/HOT, WAL/checkpoint, tablespaces, TOAST, extensions (pg_trgm, FTS), мониторинг pg_stat*.

**Ключевые связи:** WAL → recovery/replication; shared_buffers → hit ratio; HOT/FILLFACTOR → UPDATE performance; pg_stat_statements → tuning; GIN+tsvector → полнотекстовый поиск.

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Главы 18–20 (повторение)
2. **2-я очередь.** Новиков Б. А. и др. — Основы технологий баз данных — Главы 13–14 (повторение)
### Ключевые понятия

- **Buffer pool** — shared_buffers.
- **WAL** — durability.
- **HOT** — update optimization.
- **Extensions** — модули PostgreSQL.

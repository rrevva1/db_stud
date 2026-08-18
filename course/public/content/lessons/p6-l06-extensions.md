## Расширения PostgreSQL: установка и обзор

**Часть:** Внутреннее устройство PostgreSQL · **Модуль:** Хранение и расширения

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Установить расширение через CREATE EXTENSION
- Использовать pg_trgm и uuid-ossp
- Оценить совместимость версий

### Краткая теория

**Extensions** — упакованные модули: типы, функции, операторы, FDW.

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

**pg_trgm** — триграммы для LIKE/ similarity, GIN/GiST индексы нечёткого поиска.

**uuid-ossp** — генерация UUID (`uuid_generate_v4()`).

**pg_stat_statements** — топ SQL по времени/вызовам (нужен shared_preload_libraries).

**Полнотекстовый поиск:**
```sql
CREATE EXTENSION pg_trgm; -- fuzzy
-- tsvector/tsquery (встроено):
SELECT to_tsvector('russian', 'база данных') @@ to_tsquery('russian', 'база');
CREATE INDEX idx_fts ON docs USING GIN (to_tsvector('russian', body));
```

Совместимость: `SELECT * FROM pg_available_extensions;` — версия extension vs server.

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 20, §20.1
2. **2-я очередь.** Комаров В. И. — Путеводитель по базам данных — Раздел 13: extensions
### Ключевые понятия

- **CREATE EXTENSION** — установка модуля.
- **pg_trgm** — триграммный поиск.
- **tsvector** — лексемы полнотекстового поиска.
- **pg_stat_statements** — статистика SQL.

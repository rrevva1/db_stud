## Практика PostgreSQL

См. также: `course/sql/p5-l03-explain-analyze.sql`

### Задание 1. GIN на массив

Таблица `article(tags text[])`. Индекс GIN, запрос `@> ARRAY['sql']`. EXPLAIN до/после.

### Задание 2. JSONB

`event(payload jsonb)`. Индекс GIN с `jsonb_path_ops`. Поиск `@> '{"status":"ok"}'`.

### Задание 3. BRIN

Сгенерируйте 1M строк логов с `created_at`. BRIN на дату, запрос за последний час — сравните размер индекса с B-tree.

### Задание 4. Полнотекст

Добавьте `tsvector` (russian) на title+body. Запрос `to_tsquery('russian', 'база & данных')` с `ts_rank`.

### Самопроверка

- [ ] Правильный USING gin/gist/brin
- [ ] Оператор запроса совместим с классом операторов индекса
- [ ] EXPLAIN показывает Bitmap Index Scan / Index Scan

Сохраните: `course/sql/p5-l03-special-indexes-solution.sql`

## GIN, GiST, BRIN и полнотекстовый поиск

**Часть:** Производительность и оптимизация · **Модуль:** Индексы и планы выполнения

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Применить GIN для JSON и массивов
- Использовать BRIN для больших таблиц
- Настроить полнотекстовый поиск tsvector

### Краткая теория

#### GIN (Generalized Inverted Index)

Инвертированный индекс: «значение → список строк». Идеален для **содержимого** внутри составных типов.

```sql
-- массив тегов
CREATE INDEX idx_tags ON article USING gin (tags);

SELECT * FROM article WHERE tags @> ARRAY['sql', 'postgres'];

-- jsonb
CREATE INDEX idx_meta ON event USING gin (payload jsonb_path_ops);
SELECT * FROM event WHERE payload @> '{"type":"login"}';
```

Операторы: `@>`, `?`, `?&`, `?|` для jsonb; `@>`, `&&` для массивов.

#### GiST (Generalized Search Tree)

Гибкое дерево для **диапазонов**, **геометрии**, **полнотекста**, nearest-neighbor:

```sql
CREATE INDEX idx_period ON reservation USING gist (period);
-- period — tstzrange
SELECT * FROM reservation WHERE period && tstzrange(now(), now() + interval '1 day');
```

#### BRIN (Block Range Index)

Хранит min/max **на блок страниц** — крошечный размер, для **очень больших** таблиц с естественной корреляцией порядка (время, id):

```sql
CREATE INDEX idx_logs_time ON access_log USING brin (created_at);
```

Эффективен при `WHERE created_at BETWEEN ...` на миллиардах строк.

#### Полнотекстовый поиск

```sql
ALTER TABLE article ADD COLUMN fts tsvector
    GENERATED ALWAYS AS (to_tsvector('russian', coalesce(title,'') || ' ' || coalesce(body,''))) STORED;

CREATE INDEX idx_fts ON article USING gin (fts);

SELECT title FROM article
WHERE fts @@ to_tsquery('russian', 'postgresql & индекс');
```

`@@` — оператор совпадения; `ts_rank` — релевантность.

#### Сравнение

| Тип | Размер | Скорость записи | Применение |
|-----|--------|-----------------|------------|
| B-tree | Средний | Средняя | Скаляры |
| GIN | Большой | Медленная | JSON, массивы, FTS |
| GiST | Средний | Средняя | Диапазоны, гео |
| BRIN | Минимальный | Быстрая | Большие append-only |

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 14, §14.3
2. **2-я очередь.** Новиков Б. А. и др. — Основы технологий баз данных — Глава 11, §11.3
### Ключевые понятия

- GIN, GiST, BRIN
- `tsvector`, `to_tsquery`, `@@`
- jsonb_path_ops vs jsonb_ops

См. также: `course/sql/p5-l03-explain-analyze.sql` (сравнение планов с разными индексами)

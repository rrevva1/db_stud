## LATERAL JOIN и unnest

**Часть:** Продвинутый SQL · **Модуль:** Расширенные возможности SQL

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Использовать `LATERAL` для коррелированных подзапросов
- Развернуть массивы через `unnest`
- Упростить сложные запросы с зависимостью от внешней строки

### Краткая теория

**LATERAL** позволяет подзапросу в `FROM` ссылаться на столбцы таблиц, объявленных **слева** в том же `FROM`. Без `LATERAL` такая корреляция в `FROM` запрещена.

#### TOP-N на группу через LATERAL

```sql
SELECT d.name, top_emp.name, top_emp.salary
FROM department d
CROSS JOIN LATERAL (
    SELECT name, salary
    FROM employee e
    WHERE e.department_id = d.id
    ORDER BY salary DESC
    LIMIT 3
) AS top_emp;
```

Для каждого отдела подзапрос «видит» `d.id` и возвращает до трёх строк.

#### LATERAL vs коррелированный подзапрос в SELECT

LATERAL удобен, когда нужно **несколько столбцов** из «лучшей» строки или **несколько строк** на внешнюю запись.

#### unnest — развёртывание массивов

```sql
SELECT id, tag
FROM articles,
     unnest(tags) AS tag;
```

С `LATERAL`:

```sql
SELECT a.id, t.tag, t.ord
FROM articles a
CROSS JOIN LATERAL unnest(a.tags) WITH ORDINALITY AS t(tag, ord);
```

`WITH ORDINALITY` добавляет порядковый номер элемента в массиве.

#### jsonb_array_elements и LATERAL

```sql
SELECT o.id, item->>'sku' AS sku, (item->>'qty')::int AS qty
FROM orders o
CROSS JOIN LATERAL jsonb_array_elements(o.items) AS item;
```

#### LEFT JOIN LATERAL

Если для внешней строки подзапрос может вернуть 0 строк, используйте `LEFT JOIN LATERAL ... ON true`, чтобы сохранить строку отдела без сотрудников.

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 12, §12.3
2. **2-я очередь.** Elizabeth Noble — Pro T-SQL 2019 — Глава 4: APPLY (аналог)
### Ключевые понятия

- `CROSS JOIN LATERAL`, `LEFT JOIN LATERAL`
- `unnest`, `WITH ORDINALITY`
- Коррелированный подзапрос в секции FROM

Сквозная предметная область: **университет**, **авиакомпания** (топ рейсов по маршруту, теги багажа).

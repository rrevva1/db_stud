## Дубликаты, NULL и трёхзначная логика

**Часть:** Продвинутый SQL · **Модуль:** Расширенные возможности SQL

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Обработать NULL в условиях и агрегатах
- Найти и устранить дубликаты
- Понять семантику `NOT IN` с NULL

### Краткая теория

#### Трёхзначная логика SQL

SQL использует логику **TRUE, FALSE, UNKNOWN** (NULL в предикатах). Любое сравнение с NULL через `=` / `<>` даёт UNKNOWN, не FALSE:

```sql
SELECT NULL = NULL;   -- NULL (UNKNOWN), не TRUE
SELECT NULL IS NULL;  -- TRUE
SELECT NULL IS DISTINCT FROM NULL;  -- FALSE (PostgreSQL)
```

**WHERE** отбирает только строки, где предикат = TRUE; UNKNOWN отфильтровывается.

#### NOT IN и ловушка NULL

```sql
SELECT * FROM employee
WHERE department_id NOT IN (10, 20, NULL);
-- результат: 0 строк! Любое сравнение с NULL в списке даёт UNKNOWN
```

Безопаснее:

```sql
WHERE department_id NOT IN (10, 20)  -- без NULL в списке
-- или
WHERE NOT (department_id = ANY (ARRAY[10,20]))
-- или
WHERE department_id IS DISTINCT FROM ALL (ARRAY[10,20,NULL])
```

#### NULL в агрегатах

- `COUNT(*)` — считает все строки, включая NULL
- `COUNT(column)` — не считает NULL
- `SUM/AVG/MIN/MAX` — игнорируют NULL (кроме пустого набора → NULL)

#### COALESCE, NULLIF

```sql
COALESCE(phone, email, 'нет контакта')
NULLIF(column_a, column_b)  -- NULL если равны
```

#### Поиск дубликатов

```sql
SELECT email, COUNT(*)
FROM users
GROUP BY email
HAVING COUNT(*) > 1;
```

Полные дубликаты строк:

```sql
SELECT col1, col2, COUNT(*)
FROM t
GROUP BY col1, col2
HAVING COUNT(*) > 1;
```

#### Удаление дубликатов с сохранением одной строки

```sql
DELETE FROM users u
USING users u2
WHERE u.id > u2.id AND u.email = u2.email;
```

Или `DISTINCT ON` + пересоздание, или `ROW_NUMBER()` в CTE.

```sql
WITH ranked AS (
    SELECT id, ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS rn
    FROM users
)
DELETE FROM users WHERE id IN (SELECT id FROM ranked WHERE rn > 1);
```

#### DISTINCT ON (PostgreSQL)

```sql
SELECT DISTINCT ON (email) *
FROM users
ORDER BY email, created_at DESC;
-- одна «самая свежая» строка на email
```

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 13, §13.2
2. **2-я очередь.** К. Дж. Дейт — SQL и реляционная теория — Глава 3–4
### Ключевые понятия

- UNKNOWN, `IS NULL`, `IS DISTINCT FROM`
- NOT IN vs NOT EXISTS с NULL
- Дубликаты: GROUP BY + HAVING, ROW_NUMBER, DISTINCT ON

Сквозная предметная область: **университет**, **авиакомпания** (уникальность email пассажира).

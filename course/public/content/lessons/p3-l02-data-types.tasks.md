## Практика PostgreSQL

### Задание 1. Таблица типов

Создайте таблицу `type_lab` с минимум 8 столбцами разных типов: `INTEGER`, `NUMERIC(8,2)`, `BOOLEAN`, `VARCHAR(50)`, `TEXT`, `DATE`, `TIMESTAMP`, `JSONB`.

### Задание 2. INSERT и проверка

Вставьте 3 строки с осмысленными данными (в т.ч. одна с `NULL` в необязательном столбце). Выполните:

```sql
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'type_lab';
```

### Задание 3. SERIAL

Добавьте столбец `id SERIAL PRIMARY KEY` через новую таблицу или пересоздание. Объясните, какую sequence создал PostgreSQL.

**Справочник:** `course/sql/p3-l04-data-types.sql`

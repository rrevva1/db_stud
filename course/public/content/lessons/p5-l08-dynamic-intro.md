## Динамический SQL: concept и EXECUTE

**Часть:** Производительность и оптимизация · **Модуль:** Обслуживание и динамический SQL

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Сформировать SQL строкой в PL/pgSQL
- Выполнить EXECUTE с параметрами
- Оценить риски SQL injection

### Краткая теория

**Динамический SQL** — SQL, текст которого формируется во время выполнения. Нужен, когда имя таблицы, столбцы или условия неизвестны на этапе компиляции функции.

#### EXECUTE в PL/pgSQL

```sql
CREATE OR REPLACE FUNCTION count_rows(tab regclass)
RETURNS bigint
LANGUAGE plpgsql AS $$
DECLARE
    cnt bigint;
BEGIN
    EXECUTE format('SELECT count(*) FROM %s', tab) INTO cnt;
    RETURN cnt;
END;
$$;
```

`regclass` безопасно приводит имя к OID таблицы.

#### Параметры через USING

```sql
EXECUTE 'SELECT * FROM employee WHERE id = $1' INTO rec USING p_id;
```

Плейсхолдеры `$1, $2` — **значения** передаются отдельно от текста → защита от injection для **данных**.

#### format(), quote_ident(), quote_literal()

```sql
EXECUTE format(
    'SELECT %I FROM %I.%I WHERE status = %L',
    col_name, schema_name, table_name, status_value
);
```

- `%I` — идентификатор (quote_ident)
- `%L` — литерал (quote_literal)
- `%s` — простая подстановка (осторожно!)

**Никогда** не конкатенируйте пользовательский ввод напрямую:

```sql
-- ОПАСНО!
EXECUTE 'SELECT * FROM users WHERE name = ''' || user_input || '''';
```

#### Когда нужен динамический SQL

- Универсальные отчёты с выбором столбцов/фильтров
- DDL по расписанию (создание секций)
- Миграции, админ-утилиты

#### Prepared statements

```sql
PREPARE get_user(int) AS SELECT * FROM users WHERE id = $1;
EXECUTE get_user(42);
```

В PL/pgSQL повторный EXECUTE с одним текстом может кэшироваться планировщиком.

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 17, §17.1
2. **2-я очередь.** Edward Pollack — Dynamic SQL (2nd ed.) — Главы 1–3
### Ключевые понятия

- EXECUTE, USING, format
- quote_ident, quote_literal
- SQL injection

См. также: `course/sql/p5-l06-functions-plpgsql.sql`

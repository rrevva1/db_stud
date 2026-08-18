## Динамический SQL: шаблоны и безопасность

**Часть:** Производительность и оптимизация · **Модуль:** Обслуживание и динамический SQL

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Построить универсальный отчёт с динамическими фильтрами
- Использовать quote_ident и format
- Применить prepared statements

### Краткая теория

#### Шаблон универсального отчёта

```sql
CREATE OR REPLACE FUNCTION report_sales(
    p_date_from date,
    p_date_to   date,
    p_region    text DEFAULT NULL
)
RETURNS SETOF sales
LANGUAGE plpgsql STABLE AS $$
DECLARE
    sql text := 'SELECT * FROM sales WHERE sale_date BETWEEN $1 AND $2';
BEGIN
    IF p_region IS NOT NULL THEN
        sql := sql || ' AND region = $3';
        RETURN QUERY EXECUTE sql USING p_date_from, p_date_to, p_region;
    ELSE
        RETURN QUERY EXECUTE sql USING p_date_from, p_date_to;
    END IF;
END;
$$;
```

Альтернатива — один EXECUTE с фиксированным числом параметров и `($3 IS NULL OR region = $3)`.

#### Белый список столбцов сортировки

```sql
IF p_sort_col NOT IN ('sale_date', 'amount', 'region') THEN
    RAISE EXCEPTION 'Недопустимый столбец сортировки: %', p_sort_col;
END IF;
sql := sql || format(' ORDER BY %I', p_sort_col);
```

**Нельзя** подставлять произвольный текст пользователя в `%I` без whitelist.

#### Динамический pivot (осторожно)

Имена будущих столбцов pivot — только из справочника или whitelist, не из UI напрямую.

#### Prepared statements в приложении vs PL/pgSQL

- **Приложение:** JDBC/OCI `?` placeholders — стандарт защиты
- **PL/pgSQL:** EXECUTE ... USING; для повторяющихся запросов — PREPARE

```sql
PREPARE ins_log(text, jsonb) AS
    INSERT INTO event_log (tag, payload) VALUES ($1, $2);
EXECUTE ins_log('login', '{"ok":true}');
DEALLOCATE ins_log;
```

#### SECURITY DEFINER и dynamic SQL

Функция `SECURITY DEFINER` выполняется от имени владельца — **повышенный риск**. Обязательны:
- `SET search_path = pg_catalog, public`
- Минимальные права владельца
- Whitelist имён объектов

#### Аудит опасных паттернов

| Паттерн | Риск |
|---------|------|
| `'...' \|\| user_input` | Injection |
| `%s` с user input | Injection |
| Динамический DDL без проверки | Drop/create чужих объектов |
| SECURITY DEFINER + dynamic SQL | Эскалация привилегий |

### Что читать в источниках

1. **1-я очередь.** Elizabeth Noble — Pro T-SQL 2019 — Глава 12: dynamic SQL
2. **2-я очередь.** Edward Pollack — Dynamic SQL (2nd ed.) — Главы 4–6
### Ключевые понятия

- Whitelist идентификаторов
- SECURITY DEFINER hardening
- PREPARE / DEALLOCATE
- Универсальные отчёты

См. также: `course/sql/p5-l06-functions-plpgsql.sql`, `p5-l04-transactions-acid.sql`

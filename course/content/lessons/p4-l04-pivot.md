## PIVOT и crosstab: сводные таблицы

**Часть:** Продвинутый SQL · **Модуль:** Расширенные возможности SQL

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Построить сводную таблицу через `FILTER` и условную агрегацию
- Использовать `tablefunc.crosstab`
- Сравнить подходы pivot / unpivot

### Краткая теория

**Сводная таблица (pivot)** превращает значения строкового столбца в отдельные столбцы. В PostgreSQL нет оператора `PIVOT` как в Excel или T-SQL; pivot делают через агрегацию.

#### Условная агрегация с FILTER

```sql
SELECT
    department,
    SUM(amount) FILTER (WHERE quarter = 'Q1') AS q1,
    SUM(amount) FILTER (WHERE quarter = 'Q2') AS q2,
    SUM(amount) FILTER (WHERE quarter = 'Q3') AS q3,
    SUM(amount) FILTER (WHERE quarter = 'Q4') AS q4
FROM sales
GROUP BY department;
```

Эквивалент через `CASE`:

```sql
SUM(CASE WHEN quarter = 'Q1' THEN amount ELSE 0 END) AS q1
```

#### crosstab из расширения tablefunc

```sql
CREATE EXTENSION IF NOT EXISTS tablefunc;

SELECT *
FROM crosstab(
    'SELECT department, quarter, amount
     FROM sales ORDER BY 1, 2',
    'SELECT DISTINCT quarter FROM sales ORDER BY 1'
) AS ct(department text, q1 numeric, q2 numeric, q3 numeric, q4 numeric);
```

Первый аргумент — SQL «длинного» формата `(row_name, category, value)`; второй — список категорий (столбцов).

#### crosstab2 — с автоматическими категориями

Если набор категорий заранее неизвестен, используйте двухаргументный `crosstab` или динамический SQL.

#### UNPIVOT (длинный формат)

Обратная операция — из широкой таблицы в `(ключ, атрибут, значение)`:

```sql
SELECT department, 'Q1' AS quarter, q1 AS amount FROM pivot_table
UNION ALL
SELECT department, 'Q2', q2 FROM pivot_table
-- ...
;
```

В PostgreSQL 14+ удобен `UNPIVOT` через `LATERAL` и `VALUES`, либо `jsonb_each`.

#### Когда что использовать

| Подход | Плюсы | Минусы |
|--------|-------|--------|
| FILTER / CASE | Без расширений, явные столбцы | Много кода при многих категориях |
| crosstab | Компактно для отчётов | Нужен tablefunc, фиксированная схема результата |
| Приложение / BI | Гибкий pivot | Вне SQL |

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 12, §12.4
2. **2-я очередь.** Ицик Бен-Ган и др. — Microsoft SQL Server 2012. Создание запросов — Глава 8: pivot
### Ключевые понятия

- Pivot / unpivot, long vs wide format
- `FILTER (WHERE ...)`, `CASE`
- `tablefunc.crosstab`

Сквозная предметная область: **университет** (оценки по семестрам), **авиакомпания** (продажи по месяцам).

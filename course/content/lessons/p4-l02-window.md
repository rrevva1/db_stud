## Оконные функции: OVER, PARTITION BY, ROWS

**Часть:** Продвинутый SQL · **Модуль:** Расширенные возможности SQL

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Применить `ROW_NUMBER`, `RANK`, `DENSE_RANK`
- Задать рамку окна `ROWS` / `RANGE`
- Вычислить скользящие агрегаты

### Краткая теория

**Оконная функция** вычисляет значение для каждой строки на основе «окна» — набора строк, связанных с текущей. В отличие от `GROUP BY`, строки **не схлопываются**: каждая строка результата сохраняется.

#### Синтаксис

```sql
функция(...) OVER (
    [PARTITION BY столбец1, ...]
    [ORDER BY столбец1 [ASC|DESC], ...]
    [frame_clause]
)
```

#### Функции ранжирования

```sql
SELECT
    name,
    department_id,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rn,
    RANK()       OVER (PARTITION BY department_id ORDER BY salary DESC) AS rnk,
    DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS drnk
FROM employee;
```

- `ROW_NUMBER` — уникальный номер (1, 2, 3, 4)
- `RANK` — с пропусками при равенстве (1, 2, 2, 4)
- `DENSE_RANK` — без пропусков (1, 2, 2, 3)

#### Смещение: LAG / LEAD

```sql
SELECT
    order_date,
    amount,
    LAG(amount, 1) OVER (ORDER BY order_date) AS prev_amount,
    LEAD(amount, 1) OVER (ORDER BY order_date) AS next_amount
FROM sales;
```

#### Рамка окна (frame)

По умолчанию при `ORDER BY` рамка — `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`.

**Скользящее среднее за 3 строки:**

```sql
SELECT
    order_date,
    amount,
    AVG(amount) OVER (
        ORDER BY order_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3
FROM sales;
```

`ROWS` считает физические строки; `RANGE` — логический диапазон по значению `ORDER BY`.

#### Оконные агрегаты vs GROUP BY

`SUM(...) OVER (...)` сохраняет детализацию; `SUM(...) ... GROUP BY` сворачивает строки.

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 12, §12.2
2. **2-я очередь.** Ицик Бен-Ган и др. — Microsoft SQL Server 2012. Создание запросов — Глава 7: оконные функции
### Ключевые понятия

- `OVER`, `PARTITION BY`, `ORDER BY`, frame clause
- `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `LEAD`, `NTILE`
- Скользящие агрегаты, накопительные суммы

Сквозная предметная область: **университет** и **авиакомпания** (рейтинги, продажи билетов по датам).

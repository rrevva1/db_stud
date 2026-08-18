## CTE: WITH и рекурсивные запросы

**Часть:** Продвинутый SQL · **Модуль:** Расширенные возможности SQL

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Оформить запрос с общим табличным выражением (CTE)
- Построить рекурсивный CTE для иерархий
- Сравнить CTE и вложенные подзапросы

### Краткая теория

**Общее табличное выражение (CTE)** — именованный подзапрос, объявляемый через `WITH` перед основным `SELECT`. CTE существует только в рамках одного SQL-оператора и делает многошаговые запросы читаемыми.

#### Нерекурсивный CTE

```sql
WITH dept_avg AS (
    SELECT department_id, AVG(salary) AS avg_sal
    FROM employee
    GROUP BY department_id
)
SELECT e.name, e.salary, d.avg_sal
FROM employee e
JOIN dept_avg d ON d.department_id = e.department_id
WHERE e.salary > d.avg_sal;
```

Несколько CTE перечисляются через запятую; каждый следующий может ссылаться на предыдущие.

#### Рекурсивный CTE

Состоит из **якорной** части (базовые строки) и **рекурсивной** части, соединённых через `UNION ALL`:

```sql
WITH RECURSIVE org_tree AS (
    -- якорь: корень иерархии
    SELECT id, name, manager_id, 1 AS level
    FROM employee
    WHERE manager_id IS NULL
    UNION ALL
    -- рекурсия: дети текущего уровня
    SELECT e.id, e.name, e.manager_id, t.level + 1
    FROM employee e
    JOIN org_tree t ON e.manager_id = t.id
)
SELECT * FROM org_tree ORDER BY level, name;
```

PostgreSQL 14+ поддерживает `SEARCH DEPTH FIRST` / `BREADTH FIRST` для упорядочивания обхода и `CYCLE` для обнаружения циклов в графах.

#### CTE vs подзапрос

| Критерий | CTE | Подзапрос |
|----------|-----|-----------|
| Читаемость | Высокая при нескольких шагах | Ухудшается при вложенности |
| Повторное использование | Да, в том же запросе | Нужно дублировать |
| План выполнения | Может материализоваться (`MATERIALIZED`) | Обычно встраивается |

Оптимизатор PostgreSQL не гарантирует, что CTE «быстрее» — иногда `NOT MATERIALIZED` даёт лучший план, чем материализация по умолчанию.

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 12, §12.1
2. **2-я очередь.** К. Дж. Дейт — SQL и реляционная теория — Глава 7
### Ключевые понятия

- `WITH`, `WITH RECURSIVE`, якорь, рекурсивная часть
- Материализация CTE (`MATERIALIZED` / `NOT MATERIALIZED`)
- Применение: иерархии, графы, многошаговая аналитика

Сквозная предметная область: **университет** (`student`, `s_group`, `performance`) и проект **авиакомпания**.

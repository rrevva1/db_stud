## Updatable views, правила и INSTEAD OF

**Часть:** Продвинутый SQL · **Модуль:** Расширенные возможности SQL

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Создать обновляемое представление (updatable view)
- Применить правила (rules) в PostgreSQL
- Разделить логику доступа через представления

### Краткая теория

**Представление (VIEW)** — сохранённый запрос с именем. PostgreSQL может автоматически **переписывать** INSERT/UPDATE/DELETE через простые представления на одну таблицу.

#### Простое обновляемое VIEW

```sql
CREATE VIEW active_employees AS
SELECT id, name, department_id, salary
FROM employee
WHERE fired_at IS NULL;

UPDATE active_employees
SET salary = salary * 1.05
WHERE department_id = 10;
-- PostgreSQL преобразует в UPDATE employee ...
```

Условия автообновляемости (упрощённо): одна базовая таблица в FROM, без DISTINCT/GROUP BY/HAVING/UNION, без агрегатов и оконных функций.

Проверка: `information_schema.views` и `pg_views`; для деталей — `pg_rewrite`.

#### WITH CHECK OPTION

```sql
CREATE VIEW dept_10_only AS
SELECT * FROM employee WHERE department_id = 10
WITH CHECK OPTION;

-- INSERT с department_id = 20 будет отклонён
```

#### Сложные VIEW — INSTEAD OF триггеры

Когда VIEW не обновляем автоматически (JOIN, агрегаты), используют триггер:

```sql
CREATE VIEW emp_dept AS
SELECT e.id, e.name, d.name AS dept_name
FROM employee e JOIN department d ON d.id = e.department_id;

CREATE OR REPLACE FUNCTION emp_dept_update()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    UPDATE employee SET name = NEW.name WHERE id = OLD.id;
    RETURN NEW;
END;
$$;

CREATE TRIGGER emp_dept_u INSTEAD OF UPDATE ON emp_dept
FOR EACH ROW EXECUTE FUNCTION emp_dept_update();
```

#### Rules (правила) — устаревающий механизм

```sql
CREATE RULE emp_ins AS ON INSERT TO emp_view DO INSTEAD
    INSERT INTO employee (name, dept_id) VALUES (NEW.name, NEW.dept_id);
```

Rules переписывают запрос **до** планирования. Сейчас чаще используют триггеры INSTEAD OF или RLS. Rules всё ещё встречаются в legacy-схемах и для `ON SELECT DO ALSO` (материализация логов).

#### VIEW vs MATERIALIZED VIEW

Обычное VIEW всегда актуально; MATERIALIZED VIEW хранит снимок и требует `REFRESH`.

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 13, §13.1
2. **2-я очередь.** К. Дж. Дейт — SQL и реляционная теория — Глава 9
### Ключевые понятия

- Updatable view, `WITH CHECK OPTION`
- `INSTEAD OF` триггеры
- Rules vs triggers
- View updating problem (теория Дейта)

Сквозная предметная область: **университет** (представление «активные студенты»), **авиакомпания** (VIEW бронирований).

## Представления (VIEW) и материализованные представления

**Часть:** SQL: язык манипулирования и определения данных · **Модуль:** Функции, транзакции и объекты БД

Практика выполняется в **PostgreSQL** (psql или pgAdmin). Сквозная предметная область — **университет** (студенты, группы, оценки).

### Цели урока

- Создать обычное и материализованное VIEW
- Обновлять данные через представления
- Применить REFRESH MATERIALIZED VIEW

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 11, §11.1
2. **2-я очередь.** Братусь Н. В. и др. — Базы данных. Практикум — Глава 7: представления

Далее (по желанию):

- Уолтер Шилдс — SQL: быстрое погружение — Глава 9: представление как сохранённый запрос

### Краткая теория

**Представление** (VIEW) — **сохранённый запрос** SELECT, к которому можно обратиться как к таблице: вместо того чтобы каждый раз вставлять тот же подзапрос, вы пишете `SELECT … FROM v_student_groups`.

#### Создание VIEW

```sql
CREATE VIEW v_student_groups AS
SELECT s.student_id, s.last_name, s.first_name, g.name AS group_name
FROM student s
JOIN student_in_group sig ON sig.student_id = s.student_id
JOIN s_group g ON g.group_id = sig.group_id;

SELECT * FROM v_student_groups WHERE group_name = 'ИВТ-21';
```

`CREATE OR REPLACE VIEW` обновляет определение, не трогая базовые таблицы. `DROP VIEW v_student_groups` удаляет **только** объект представления: строки `student` остаются. Если на VIEW ссылаются другие объекты, удаление может потребовать `CASCADE` и сломает зависимые запросы.

Два представления можно соединить JOIN, если в каждом сохранены общие ключи (например, `student_id`).

#### Обновляемые представления

Простые VIEW над одной таблицей без агрегатов могут поддерживать INSERT/UPDATE/DELETE. Сложные — через **INSTEAD OF** триггеры (Part 4).

#### Материализованное представление

```sql
CREATE MATERIALIZED VIEW mv_group_stats AS
SELECT g.name, COUNT(sig.student_id) AS cnt, AVG(p.grade) AS avg_grade
FROM s_group g
LEFT JOIN student_in_group sig ON sig.group_id = g.group_id
LEFT JOIN performance p ON p.student_id = sig.student_id
GROUP BY g.name;

REFRESH MATERIALIZED VIEW mv_group_stats;
```

Данные хранятся физически; обновление — явным `REFRESH`.

#### Зачем нужны VIEW

- Упрощение запросов для пользователей.
- Разграничение доступа (GRANT на VIEW, не на таблицы).
- Абстракция от изменений схемы.

Справочник: `course/sql/p3-l22-lab-university.sql`.

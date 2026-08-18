# -*- coding: utf-8 -*-
TASKS = {}

TASKS["p3-l01-create-table"] = """## Практика PostgreSQL

**Подготовка:** выполните `\\i course/sql/schema-university.sql` или создайте схему `lab` самостоятельно.

### Задание 1. Схема и таблицы

Создайте схему `lab` и таблицы `student`, `s_group`, `student_in_group` по образцу из `course/sql/p3-l01-create-tables.sql`. Добавьте комментарии к таблицам.

### Задание 2. IF NOT EXISTS

Напишите скрипт, который можно запускать повторно без ошибок (используйте `IF NOT EXISTS`).

### Задание 3. Проверка

Выполните `\\d lab.student` и `\\d lab.s_group` в psql. Убедитесь, что первичные ключи созданы.

### Самопроверка

- [ ] Три таблицы созданы в схеме `lab`
- [ ] `student_in_group` имеет составной PRIMARY KEY
- [ ] Скрипт идемпотентен

**Решение сохраните в:** `course/sql/p3-l01-create-table-solution.sql`
"""

TASKS["p3-l02-data-types"] = """## Практика PostgreSQL

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
"""

TASKS["p3-l03-constraints"] = """## Практика PostgreSQL

### Задание 1. Ограничения на performance

На схеме `university` добавьте (если нет) `CHECK (grade BETWEEN 2 AND 5)` и `UNIQUE (student_id, subject_id, grade_date)`.

### Задание 2. Нарушение FK

Попробуйте вставить в `student_in_group` несуществующий `student_id`. Зафиксируйте текст ошибки и SQLSTATE.

### Задание 3. CASCADE

Создайте тестовую таблицу с `ON DELETE CASCADE`. Удалите родительскую строку и проверьте дочерние.

**Справочник:** `course/sql/p3-l06-ddl-constraints.sql`
"""

TASKS["p3-l04-alter-table"] = """## Практика PostgreSQL

### Задание 1. Новый столбец

```sql
ALTER TABLE university.student ADD COLUMN phone VARCHAR(20);
UPDATE university.student SET phone = '+7-900-000-00-01' WHERE student_id = 1;
```

### Задание 2. NOT NULL

Заполните `phone` для всех студентов, затем `ALTER COLUMN phone SET NOT NULL`.

### Задание 3. Переименование

Переименуйте столбец `phone` в `phone_number`. Переименуйте таблицу `type_lab` → `type_lab_archive` (если создавали на прошлом уроке).

### Задание 4. DROP

Удалите столбец `phone_number` командой `DROP COLUMN IF EXISTS`.
"""

TASKS["p3-l05-insert"] = """## Практика PostgreSQL

**Данные:** схема `university` после `schema-university.sql`.

### Задание 1. Один студент

```sql
INSERT INTO student (last_name, first_name, birth_date, email)
VALUES ('Новиков', 'Дмитрий', '2004-03-01', 'novikov@uni.local')
RETURNING student_id;
```

### Задание 2. Пакетная вставка

Добавьте 3 группы и 5 студентов одним `INSERT ... VALUES (...), (...), ...`.

### Задание 3. INSERT ... SELECT

Скопируйте всех студентов группы `ИВТ-21` в таблицу `student_ивт21` (создайте её как `CREATE TABLE ... AS SELECT ...`).

**Справочник:** `course/sql/p3-l02-insert-select.sql`
"""

TASKS["p3-l06-update"] = """## Практика PostgreSQL

### Задание 1. Точечное обновление

Обновите email студента с `student_id = 1`. Используйте `RETURNING`.

### Задание 2. UPDATE ... FROM

Повысьте на 1 балл все оценки студентов группы `ИВТ-21`, где оценка = 4 (не выше 5):

```sql
UPDATE performance p
SET grade = grade + 1
FROM student_in_group sig
JOIN s_group g ON g.group_id = sig.group_id
WHERE ...
```

### Задание 3. Безопасность

Сначала выполните `SELECT` с тем же условием, что и UPDATE. Сколько строк будет затронуто?
"""

TASKS["p3-l07-delete"] = """## Практика PostgreSQL

### Задание 1. DELETE с WHERE

Удалите тестового студента «Новиков» (если создавали). Используйте `RETURNING`.

### Задание 2. CASCADE

Удалите студента, состоящего в группе. Проверьте, удалилась ли запись в `student_in_group`.

### Задание 3. TRUNCATE

На копии таблицы `performance` выполните `TRUNCATE ... RESTART IDENTITY`. Сравните время/поведение с `DELETE FROM performance`.

### Вопрос для отчёта

Когда предпочтительнее TRUNCATE, а когда DELETE?
"""

TASKS["p3-l08-select-basics"] = """## Практика PostgreSQL

**Загрузите данные:** `\\i course/sql/p3-l22-lab-university.sql`

### Задание 1. Базовый SELECT

Выведите фамилию, имя и email всех студентов с псевдонимами на русском.

### Задание 2. DISTINCT

Список уникальных курсов (`course_num`) среди групп.

### Задание 3. LIMIT/OFFSET

Третья «страница» списка студентов (по 2 записи), отсортированного по фамилии.

### Задание 4. Выражения

Выведите ФИО одной строкой (`CONCAT` или `||`) и год рождения через `EXTRACT`.
"""

TASKS["p3-l09-where-order"] = """## Практика PostgreSQL

### Задание 1. Фильтрация

Студенты, родившиеся в 2004 году (`BETWEEN` или `EXTRACT`).

### Задание 2. LIKE и IN

Группы с именем на `И%` и курс IN (2, 3).

### Задание 3. NULL

Все студенты **без** email (`IS NULL`).

### Задание 4. Сортировка

Оценки по дисциплине «Базы данных»: сначала по убыванию балла, затем по фамилии студента (нужен JOIN).
"""

TASKS["p3-l10-joins-intro"] = """## Практика PostgreSQL

### Задание 1. Три таблицы

Напишите запрос: фамилия студента, название группы, номер курса (JOIN student → student_in_group → s_group).

### Задание 2. USING

Перепишите фрагмент с `ON sig.student_id = s.student_id` через `USING (student_id)` где возможно.

### Задание 3. Концептуальный вопрос

Объясните, почему нельзя получить название группы одним SELECT только из `student` без JOIN.
"""

TASKS["p3-l11-inner-join"] = """## Практика PostgreSQL

### Задание 1. Студенты и оценки

Список: фамилия, дисциплина, оценка (INNER JOIN трёх таблиц).

### Задание 2. Фильтр после JOIN

Только отличники (оценка = 5) по «Базам данных».

### Задание 3. Читаемость

Перепишите запрос из задания 1, используя осмысленные алиасы (`s`, `p`, `subj`).

**Справочник:** `course/sql/p3-l14-joins.sql`
"""

TASKS["p3-l12-outer-join"] = """## Практика PostgreSQL

### Задание 1. Все группы

LEFT JOIN: название группы и фамилия студента (включая группы без студентов).

### Задание 2. Anti-join

Группы, в которых **нет ни одного** студента (`HAVING COUNT = 0` или `WHERE student_id IS NULL`).

### Задание 3. FULL OUTER

Студенты без группы и группы без студентов (одним запросом с FULL JOIN — если такие данные есть, иначе смоделируйте).

### Отчёт

Когда вы бы выбрали LEFT, а когда INNER для отчёта деканата?
"""

TASKS["p3-l13-cross-self-join"] = """## Практика PostgreSQL

### Задание 1. CROSS JOIN

Сколько строк даст `CROSS JOIN` между `student` (4 строки) и `s_group` (3 строки)? Проверьте запросом.

### Задание 2. SELF JOIN

Пары студентов с одинаковой фамилией (если нет — добавьте тестовую строку).

### Задание 3. Иерархия

Создайте таблицу `employee(emp_id, name, manager_id)` с 5 сотрудниками. Выведите сотрудник — руководитель через SELF JOIN.
"""

TASKS["p3-l14-group-by"] = """## Практика PostgreSQL

### Задание 1. Средний балл

По каждой дисциплине: название, число оценок, средний балл (округлить до 2 знаков).

### Задание 2. Студенты в группах

Число студентов в каждой группе (`COUNT`).

### Задание 3. MIN/MAX

Дисциплина с наибольшим разбросом оценок (`MAX - MIN`).

**Справочник:** `course/sql/p3-l17-group-by.sql`
"""

TASKS["p3-l15-having"] = """## Практика PostgreSQL

### Задание 1. Группы с высоким средним

Группы, где средний балл студентов ≥ 4.0 (JOIN + GROUP BY + HAVING).

### Задание 2. WHERE + HAVING

Средний балл по дисциплинам только для оценок не ниже 3 (`WHERE grade >= 3`) и только дисциплины с ≥ 3 оценками (`HAVING COUNT(*) >= 3`).

### Задание 3. Объяснение

Почему условие `AVG(grade) >= 4` нельзя поставить в WHERE?
"""

TASKS["p3-l16-subqueries"] = """## Практика PostgreSQL

### Задание 1. Scalar

Студенты с оценкой выше общего среднего по всем дисциплинам.

### Задание 2. IN

Список студентов группы `ПМИ-21` (через подзапрос, без JOIN в основном FROM).

### Задание 3. EXISTS

Дисциплины, по которым **нет ни одной** оценки ниже 4 (NOT EXISTS плохих оценок).

### Задание 4. FROM

Средний балл по группам — подзапрос во FROM + JOIN с `s_group`.

**Справочник:** `course/sql/p3-l19-subqueries.sql`
"""

TASKS["p3-l17-set-ops"] = """## Практика PostgreSQL

### Задание 1. UNION

Объедините фамилии студентов и преподавателей в один список (`UNION`).

### Задание 2. INTERSECT

`student_id` студентов, у которых есть и оценка 5, и оценка 3.

### Задание 3. EXCEPT

Студенты, у которых нет ни одной оценки (через EXCEPT или альтернативу NOT EXISTS).

### Задание 4. UNION ALL

Повторите задание 1 с `UNION ALL` — сравните число строк.
"""

TASKS["p3-l18-scalar-funcs"] = """## Практика PostgreSQL

### Задание 1. Строки

Для каждого студента: `UPPER(last_name)`, длина email, `COALESCE(email, 'не указан')`.

### Задание 2. Даты

Возраст студента в годах (`AGE` или `EXTRACT`).

### Задание 3. Числа

По дисциплинам: `ROUND(AVG(grade), 2)`, `MIN`, `MAX`.

### Задание 4. NULLIF

Столбец «отличие от 5»: `NULLIF(5 - grade, 0)` — что даёт для отличников?
"""

TASKS["p3-l19-case-when"] = """## Практика PostgreSQL

### Задание 1. Текстовая оценка

CASE: 5→«отлично», 4→«хорошо», 3→«удовл.», иначе «неуд» для всех записей performance.

### Задание 2. CAST

Средний балл как `numeric(4,2)` и как текст (`::text`).

### Задание 3. Условная агрегация

По группам: число отличников (5) и число неудов (2) в одном SELECT через `COUNT(CASE WHEN ...)`.
"""

TASKS["p3-l20-transactions"] = """## Практика PostgreSQL

### Задание 1. Перевод между «счетами»

Создайте `account(id, balance)`. Две строки по 1000. В одной транзакции переведите 200 с id=1 на id=2. Проверьте балансы после COMMIT.

### Задание 2. ROLLBACK

Повторите перевод, но выполните ROLLBACK. Балансы должны вернуться.

### Задание 3. SAVEPOINT

INSERT студента → SAVEPOINT → DELETE → ROLLBACK TO SAVEPOINT → COMMIT. Студент должен остаться.

### Отчёт

Опишите ACID на примере задания 1.
"""

TASKS["p3-l21-isolation"] = """## Практика PostgreSQL

**Нужны две сессии psql.**

### Задание 1. READ COMMITTED

Сессия 1: BEGIN; UPDATE student SET email = 'test1@x.local' WHERE student_id = 1; (не COMMIT).
Сессия 2: SELECT email для student_id = 1 — какое значение? COMMIT в сессии 1; повторите SELECT.

### Задание 2. REPEATABLE READ

Сессия 1: BEGIN ISOLATION LEVEL REPEATABLE READ; SELECT COUNT(*) FROM student;
Сессия 2: INSERT нового студента; COMMIT;
Сессия 1: SELECT COUNT(*) снова — изменилось ли?

### Задание 3. Теория

Кратко опишите phantom read и как его предотвращает REPEATABLE READ в PostgreSQL.
"""

TASKS["p3-l22-views"] = """## Практика PostgreSQL

### Задание 1. VIEW

```sql
CREATE VIEW v_student_avg AS
SELECT s.student_id, s.last_name, AVG(p.grade)::numeric(4,2) AS avg_grade
FROM student s
LEFT JOIN performance p ON p.student_id = s.student_id
GROUP BY s.student_id, s.last_name;
```

### Задание 2. Использование

`SELECT * FROM v_student_avg WHERE avg_grade >= 4.5 ORDER BY avg_grade DESC;`

### Задание 3. MATERIALIZED VIEW

Создайте MV для статистики по группам. Измените данные, выполните REFRESH — сравните результат до и после.

**Справочник:** `course/sql/p3-l22-lab-university.sql`
"""

TASKS["p3-l23-triggers"] = """## Практика PostgreSQL

### Задание 1. Таблица аудита

```sql
CREATE TABLE student_audit (
    audit_id SERIAL PRIMARY KEY,
    student_id INT,
    action TEXT,
    changed_at TIMESTAMP DEFAULT NOW()
);
```

### Задание 2. Функция и триггер

AFTER INSERT OR UPDATE OR DELETE на `student` — запись в `student_audit` с `TG_OP`.

### Задание 3. Тест

INSERT, UPDATE, DELETE одного студента. Проверьте 3 строки в audit.

### Вопрос

Чем BEFORE отличается от AFTER для аудита?
"""

TASKS["p3-l24-exam"] = """## Итоговый контроль PostgreSQL

**Время:** 90 минут · **Схема:** `university` (полная загрузка из `p3-l22-lab-university.sql`)

### Часть A. DDL (20 баллов)

1. Создайте таблицу `scholarship(student_id, amount, from_date)` с FK на student и CHECK amount > 0.
2. Добавьте столбец `note TEXT` через ALTER TABLE.

### Часть B. DML (15 баллов)

3. INSERT стипендии 5000 для двух студентов с RETURNING.
4. UPDATE: увеличьте amount на 10% тем, у кого средний балл ≥ 4.5.
5. DELETE стипендий студентов без оценок (подзапрос).

### Часть C. SELECT (35 баллов)

6. INNER JOIN: фамилия, группа, дисциплина, оценка для курса 3.
7. LEFT JOIN: все группы и число студентов.
8. GROUP BY + HAVING: дисциплины со средним ≥ 4 и ≥ 2 оценок.
9. Подзапрос EXISTS: студенты с хотя бы одной «5».
10. UNION: фамилии студентов и преподавателей.

### Часть D. Транзакции и VIEW (20 баллов)

11. Транзакция: INSERT оценки + INSERT audit в одном COMMIT; ROLLBACK в втором прогоне.
12. CREATE VIEW `v_deans_report` — группа, средний балл, число студентов.

### Часть E. Теория (10 баллов)

13. WHERE vs HAVING; INNER vs LEFT JOIN; DELETE vs TRUNCATE — краткие определения.

**Сохраните решение:** `course/sql/p3-l24-exam-solution.sql`
"""

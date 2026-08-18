# -*- coding: utf-8 -*-
"""Theory content for Part 3 lessons."""
THEORY = {}

THEORY["p3-l01-create-table"] = """### Краткая теория

**DDL** (Data Definition Language) — подмножество SQL для описания структуры базы данных. Команда `CREATE TABLE` создаёт новое **отношение** (таблицу) с именованными **столбцами** (атрибутами) и их типами.

#### Синтаксис CREATE TABLE

```sql
CREATE TABLE [IF NOT EXISTS] имя_таблицы (
    столбец1 тип_данных [ограничения],
    столбец2 тип_данных [ограничения],
    ...
);
```

В PostgreSQL объекты организуются в **схемы** (`schema`). Схема `public` используется по умолчанию; для учебных проектов удобно создавать отдельную схему:

```sql
CREATE SCHEMA IF NOT EXISTS university;
SET search_path TO university, public;
```

#### Пример: таблицы студент и группа

```sql
CREATE TABLE student (
    student_id   SERIAL PRIMARY KEY,
    last_name    VARCHAR(50) NOT NULL,
    first_name   VARCHAR(50) NOT NULL,
    birth_date   DATE NOT NULL
);

CREATE TABLE s_group (
    group_id     SERIAL PRIMARY KEY,
    name         VARCHAR(20) NOT NULL UNIQUE,
    course_num   SMALLINT NOT NULL
);
```

`SERIAL` — псевдотип PostgreSQL: целое число с автоматически создаваемой последовательностью (аналог автоинкремента).

#### IF NOT EXISTS и комментарии

`CREATE TABLE IF NOT EXISTS` предотвращает ошибку при повторном запуске скрипта. Документирование:

```sql
COMMENT ON TABLE student IS 'Студенты университета';
COMMENT ON COLUMN student.birth_date IS 'Дата рождения';
```

#### Связующая таблица

Связь «студент — группа» многие-ко-многим реализуется таблицей `student_in_group`:

```sql
CREATE TABLE student_in_group (
    student_id   INT NOT NULL REFERENCES student(student_id),
    group_id     INT NOT NULL REFERENCES s_group(group_id),
    enrolled_at  DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (student_id, group_id)
);
```

#### Ключевые понятия

| Понятие | Описание |
|---------|----------|
| Отношение | Таблица в реляционной модели |
| Столбец (атрибут) | Именованное поле с фиксированным типом |
| Схема | Пространство имён для таблиц и других объектов |
| DDL | CREATE, ALTER, DROP — определение структуры |

> **Связь с теорией:** таблица SQL — физическая реализация отношения из реляционной модели (Part 1). Проектирование ER-модели (Part 2) предшествует написанию DDL.

Справочный скрипт: `course/sql/p3-l01-create-tables.sql`, базовая схема: `course/sql/schema-university.sql`.
"""

THEORY["p3-l02-data-types"] = """### Краткая теория

Каждый столбец таблицы имеет **тип данных** — множество допустимых значений (домен). Правильный выбор типа обеспечивает **доменную целостность** и влияет на производительность и объём хранения.

#### Числовые типы

| Тип | Назначение |
|-----|------------|
| `SMALLINT`, `INTEGER`, `BIGINT` | Целые числа разной разрядности |
| `NUMERIC(p,s)`, `DECIMAL(p,s)` | Точные десятичные (деньги, оценки) |
| `REAL`, `DOUBLE PRECISION` | Числа с плавающей точкой (приближённые) |
| `SERIAL`, `BIGSERIAL` | Автоинкремент (целое + sequence) |

```sql
CREATE TABLE account (
    id      SERIAL PRIMARY KEY,
    balance NUMERIC(12, 2) NOT NULL DEFAULT 0
);
```

#### Символьные типы

- `CHAR(n)` — фиксированная длина (дополняется пробелами).
- `VARCHAR(n)` — переменная длина с ограничением.
- `TEXT` — строка неограниченной длины.

В PostgreSQL **нет практической разницы** в производительности между `TEXT` и `VARCHAR(n)`; ограничение длины задаёт `VARCHAR(n)` на уровне схемы.

#### Дата и время

```sql
birth_date   DATE,                          -- только дата
created_at   TIMESTAMP DEFAULT NOW(),       -- дата + время
updated_at   TIMESTAMPTZ,                   -- с часовым поясом
duration     INTERVAL                       -- интервал
```

#### Логический и специальные типы

```sql
is_active BOOLEAN DEFAULT TRUE,
tags      TEXT[],
payload   JSONB
```

`JSONB` удобен для полуструктурированных данных; для строгой модели предпочтительна нормализованная схема.

#### NULL

Любой тип допускает `NULL`, если столбец не объявлен `NOT NULL`. `NULL` — отсутствие значения, не ноль и не пустая строка.

Справочник: `course/sql/p3-l04-data-types.sql`.
"""

THEORY["p3-l03-constraints"] = """### Краткая теория

**Ограничения целостности** (constraints) — правила, которые СУБД проверяет при каждой операции INSERT/UPDATE. Они реализуют сущностную, ссылочную и доменную целостность.

#### PRIMARY KEY — первичный ключ

Уникально идентифицирует строку; не допускает NULL:

```sql
student_id SERIAL PRIMARY KEY
-- или составной:
PRIMARY KEY (student_id, group_id)
```

#### FOREIGN KEY — внешний ключ

Столбец (или набор столбцов) ссылается на PRIMARY KEY или UNIQUE другой таблицы:

```sql
group_id INT NOT NULL REFERENCES s_group(group_id)
    ON DELETE CASCADE
    ON UPDATE RESTRICT
```

| Действие | Поведение при удалении родителя |
|----------|-------------------------------|
| `RESTRICT` / `NO ACTION` | Запрет удаления |
| `CASCADE` | Каскадное удаление дочерних строк |
| `SET NULL` | Обнуление внешнего ключа |

#### UNIQUE, NOT NULL, CHECK

```sql
email VARCHAR(100) UNIQUE,
course_num SMALLINT NOT NULL CHECK (course_num BETWEEN 1 AND 6),
salary NUMERIC CHECK (salary > 0)
```

#### Именованные ограничения

```sql
CONSTRAINT chk_grade CHECK (grade BETWEEN 2 AND 5)
```

Имена упрощают диагностику ошибок:

```
ERROR: new row violates check constraint "chk_grade"
```

#### Обработка нарушений

При нарушении ограничения PostgreSQL откатывает операцию и возвращает ошибку. В приложении перехватывают SQLSTATE `23503` (FK), `23505` (UNIQUE), `23514` (CHECK).

Справочник: `course/sql/p3-l06-ddl-constraints.sql`.
"""

THEORY["p3-l04-alter-table"] = """### Краткая теория

Команда **ALTER TABLE** изменяет структуру существующей таблицы без пересоздания данных (в большинстве случаев).

#### Добавление и удаление столбцов

```sql
ALTER TABLE student ADD COLUMN email VARCHAR(100);
ALTER TABLE student ADD COLUMN phone VARCHAR(20) DEFAULT NULL;

ALTER TABLE student DROP COLUMN phone;
ALTER TABLE student DROP COLUMN IF EXISTS temp_col;
```

Новый столбец без DEFAULT получает NULL во всех существующих строках.

#### Изменение типа и ограничений

```sql
ALTER TABLE student ALTER COLUMN email SET NOT NULL;
ALTER TABLE student ALTER COLUMN course_num TYPE INTEGER;

-- USING нужен при несовместимом преобразовании:
ALTER TABLE student ALTER COLUMN code TYPE VARCHAR(10) USING code::VARCHAR;
```

#### Добавление ограничений

```sql
ALTER TABLE student ADD CONSTRAINT uq_email UNIQUE (email);
ALTER TABLE student ADD CONSTRAINT fk_group
    FOREIGN KEY (group_id) REFERENCES s_group(group_id);
```

#### Переименование

```sql
ALTER TABLE student RENAME COLUMN fname TO first_name;
ALTER TABLE old_students RENAME TO student_archive;
```

#### Осторожность при изменениях

- Изменение типа на большой таблице может быть долгим (перезапись).
- Добавление `NOT NULL` требует, чтобы все строки уже имели значение.
- Удаление столбца необратимо без резервной копии.

> **Практикум:** после проектирования ER-модели (Part 2) схема эволюционирует через ALTER TABLE по мере уточнения требований.
"""

THEORY["p3-l05-insert"] = """### Краткая теория

**DML** (Data Manipulation Language) — команды для работы с данными. `INSERT` добавляет новые строки в таблицу.

#### Вставка одной строки

```sql
INSERT INTO student (last_name, first_name, birth_date)
VALUES ('Иванов', 'Пётр', '2003-05-12');
```

#### Вставка нескольких строк

```sql
INSERT INTO student (last_name, first_name, birth_date) VALUES
    ('Петрова', 'Анна', '2004-01-20'),
    ('Сидоров', 'Олег', '2003-11-03');
```

#### INSERT … RETURNING

PostgreSQL возвращает вставленные данные — удобно для получения сгенерированного `SERIAL`:

```sql
INSERT INTO student (last_name, first_name, birth_date)
VALUES ('Козлова', 'Мария', '2004-07-15')
RETURNING student_id, last_name;
```

#### INSERT … SELECT

Загрузка данных из другого запроса:

```sql
INSERT INTO student_archive (student_id, last_name, first_name)
SELECT student_id, last_name, first_name
FROM student
WHERE birth_date < '2000-01-01';
```

#### DEFAULT и NULL

```sql
INSERT INTO s_group (name, course_num) VALUES ('ИВТ-23', DEFAULT);
INSERT INTO student (last_name, first_name, birth_date, email)
VALUES ('Новиков', 'Иван', '2005-03-01', NULL);
```

#### Конфликты и UPSERT

```sql
INSERT INTO student (student_id, last_name, first_name, birth_date)
VALUES (1, 'Иванов', 'Пётр', '2003-05-12')
ON CONFLICT (student_id) DO UPDATE
    SET last_name = EXCLUDED.last_name;
```

Справочник: `course/sql/p3-l02-insert-select.sql`.
"""

THEORY["p3-l06-update"] = """### Краткая теория

Команда **UPDATE** изменяет значения столбцов в существующих строках.

#### Базовый синтаксис

```sql
UPDATE student
SET email = 'ivanov@uni.local'
WHERE student_id = 1;
```

**Важно:** без `WHERE` обновляются **все** строки таблицы!

#### Обновление нескольких столбцов

```sql
UPDATE student
SET last_name = 'Иванова',
    email = 'ivanova@uni.local'
WHERE student_id = 2;
```

#### UPDATE … FROM (PostgreSQL)

Обновление на основании другой таблицы:

```sql
UPDATE performance p
SET grade = 5
FROM student s
WHERE p.student_id = s.student_id
  AND s.last_name = 'Иванов'
  AND p.grade = 4;
```

#### UPDATE … RETURNING

```sql
UPDATE student SET email = 'new@uni.local'
WHERE student_id = 1
RETURNING student_id, email;
```

#### Безопасность массовых обновлений

1. Всегда проверяйте условие `WHERE` через `SELECT` с тем же условием.
2. Используйте транзакции: `BEGIN; UPDATE ...; -- проверка; COMMIT;`
3. Ограничивайте права пользователей.

#### Связь с ограничениями

UPDATE проверяет все constraints. Попытка установить `grade = 6` при `CHECK (grade BETWEEN 2 AND 5)` завершится ошибкой.
"""

THEORY["p3-l07-delete"] = """### Краткая теория

Команды **DELETE** и **TRUNCATE** удаляют данные, но работают принципиально по-разному.

#### DELETE — построчное удаление

```sql
DELETE FROM student
WHERE student_id = 5;

DELETE FROM performance
WHERE grade_date < '2020-01-01';
```

Без `WHERE` удаляются **все** строки (таблица остаётся).

#### DELETE … RETURNING

```sql
DELETE FROM student
WHERE email IS NULL
RETURNING student_id, last_name;
```

#### Каскадное удаление

При `ON DELETE CASCADE` на внешнем ключе удаление родителя автоматически удаляет дочерние строки:

```sql
-- student_in_group с ON DELETE CASCADE
DELETE FROM student WHERE student_id = 1;
-- удалятся и записи в student_in_group
```

#### TRUNCATE — быстрая очистка

```sql
TRUNCATE TABLE performance;
TRUNCATE TABLE student_in_group, student RESTART IDENTITY CASCADE;
```

| Свойство | DELETE | TRUNCATE |
|----------|--------|----------|
| Условие WHERE | Да | Нет (вся таблица) |
| Триггеры DELETE | Срабатывают | Не срабатывают |
| Откат в транзакции | Построчно | Да (DDL в транзакции PG) |
| Скорость на больших таблицах | Медленнее | Быстрее |

#### Выбор команды

- Удалить часть строк → `DELETE` с `WHERE`.
- Полностью очистить таблицу в тестах → `TRUNCATE`.
- Удалить таблицу и структуру → `DROP TABLE`.
"""

THEORY["p3-l08-select-basics"] = """### Краткая теория

**SELECT** — основная команда SQL для выборки данных. Результат запроса — **виртуальная таблица** (набор строк и столбцов).

#### Базовый синтаксис

```sql
SELECT столбец1, столбец2
FROM   таблица;
```

Выбор всех столбцов (избегайте в production-коде):

```sql
SELECT * FROM student;
```

#### Псевдонимы (алиасы)

```sql
SELECT last_name AS фамилия,
       first_name "Имя",
       birth_date AS dob
FROM student;
```

#### DISTINCT — уникальные строки

```sql
SELECT DISTINCT course_num FROM s_group;
SELECT DISTINCT last_name, first_name FROM student;
```

`DISTINCT` применяется ко **всей** комбинации столбцов.

#### LIMIT и OFFSET — постраничная выборка

```sql
SELECT last_name, first_name
FROM student
ORDER BY last_name
LIMIT 10 OFFSET 20;   -- «страница 3» по 10 записей
```

#### Выражения в SELECT

```sql
SELECT last_name,
       EXTRACT(YEAR FROM birth_date) AS birth_year,
       UPPER(first_name) AS name_upper
FROM student;
```

#### Порядок выполнения (упрощённо)

1. FROM → 2. WHERE → 3. GROUP BY → 4. HAVING → 5. SELECT → 6. ORDER BY → 7. LIMIT

На этом уроке — шаги FROM, SELECT, DISTINCT, LIMIT/OFFSET.
"""

THEORY["p3-l09-where-order"] = """### Краткая теория

#### WHERE — фильтрация строк

```sql
SELECT last_name, first_name, birth_date
FROM student
WHERE birth_date >= '2004-01-01';
```

#### Логические операторы

```sql
WHERE course_num = 3 AND faculty_id = 1
WHERE last_name LIKE 'И%' OR last_name LIKE 'П%'
WHERE NOT email IS NULL
```

Приоритет: `NOT` → `AND` → `OR`. Используйте скобки для ясности.

#### Операторы сравнения

| Оператор | Пример |
|----------|--------|
| `=`, `<>`, `!=` | `grade <> 3` |
| `<`, `>`, `<=`, `>=` | `course_num >= 2` |
| `BETWEEN` | `birth_date BETWEEN '2003-01-01' AND '2004-12-31'` |
| `IN` | `group_id IN (1, 2, 5)` |
| `LIKE` | `last_name LIKE 'Иван_'` (`_` — один символ, `%` — любая строка) |
| `IS NULL` | `email IS NULL` |

> **Важно:** `WHERE email = NULL` всегда ложно! Используйте `IS NULL`.

#### ORDER BY — сортировка

```sql
SELECT last_name, first_name, birth_date
FROM student
ORDER BY last_name ASC, first_name DESC;
```

Сортировка по выражению:

```sql
ORDER BY EXTRACT(YEAR FROM birth_date), last_name;
```

`NULL` по умолчанию идут последними при `ASC` (в PostgreSQL).

#### Комбинированный пример

```sql
SELECT s.last_name, g.name
FROM student s
JOIN student_in_group sig ON sig.student_id = s.student_id
JOIN s_group g ON g.group_id = sig.group_id
WHERE g.course_num IN (2, 3)
  AND s.last_name LIKE 'И%'
ORDER BY g.name, s.last_name
LIMIT 50;
```
"""

THEORY["p3-l10-joins-intro"] = """### Краткая теория

Данные в реляционной БД распределены по **нормализованным** таблицам. **JOIN** (соединение) объединяет строки из двух и более таблиц по условию связи.

#### Зачем нужен JOIN

Таблица `student` не содержит название группы — оно в `s_group`. Связь — в `student_in_group`. Чтобы получить «студент + группа», нужно соединить три таблицы.

#### Синтаксис

```sql
SELECT s.last_name, g.name
FROM student s
INNER JOIN student_in_group sig ON sig.student_id = s.student_id
INNER JOIN s_group g ON g.group_id = sig.group_id;
```

#### ON vs USING

Если столбцы связи **имеют одинаковые имена**:

```sql
-- эквивалент ON sig.student_id = s.student_id
FROM student s
JOIN student_in_group sig USING (student_id)
```

#### Типы соединений

| Тип | Результат |
|-----|-----------|
| `INNER JOIN` | Только строки с совпадением в обеих таблицах |
| `LEFT OUTER JOIN` | Все строки левой + совпадения справа |
| `RIGHT OUTER JOIN` | Все строки правой + совпадения слева |
| `FULL OUTER JOIN` | Объединение LEFT и RIGHT |
| `CROSS JOIN` | Декартово произведение |

#### INNER vs OUTER

- **INNER** — «пересечение по условию».
- **OUTER** — сохраняет строки без пары; недостающие столбцы заполняются `NULL`.

#### Связь с реляционной алгеброй

`INNER JOIN` соответствует операции **⋈** (соединение) с условием θ. `CROSS JOIN` — декартово произведение **×**.
"""

THEORY["p3-l11-inner-join"] = """### Краткая теория

**INNER JOIN** возвращает только те строки, для которых условие соединения истинно в **обеих** таблицах.

#### Две таблицы

```sql
SELECT s.last_name, g.name AS group_name
FROM student s
INNER JOIN student_in_group sig ON sig.student_id = s.student_id
INNER JOIN s_group g ON g.group_id = sig.group_id;
```

#### Несколько таблиц

```sql
SELECT s.last_name, subj.name, p.grade
FROM performance p
JOIN student s ON s.student_id = p.student_id
JOIN subject subj ON subj.subject_id = p.subject_id
WHERE p.grade >= 4;
```

#### Составные ключи

Если связь по нескольким столбцам:

```sql
JOIN enrollment e
  ON e.student_id = s.student_id
 AND e.year = s.entry_year
```

#### Порядок JOIN и читаемость

Рекомендуется:
1. `FROM` — основная таблица (факт).
2. Последовательные `JOIN` — справочники.
3. `WHERE` — фильтрация после соединения.

#### Эквивалент через WHERE (устаревший стиль)

```sql
SELECT s.last_name, g.name
FROM student s, student_in_group sig, s_group g
WHERE sig.student_id = s.student_id
  AND g.group_id = sig.group_id;
```

Явный `JOIN` предпочтительнее: условие связи отделено от фильтрации.

#### План выполнения

СУБД может менять порядок соединений. На больших таблицах важны индексы на столбцах FK (Part 5).

Справочник: `course/sql/p3-l14-joins.sql`.
"""

THEORY["p3-l12-outer-join"] = """### Краткая теория

**Внешние соединения** (OUTER JOIN) сохраняют строки «без пары» из одной или обеих таблиц.

#### LEFT OUTER JOIN

Все строки из **левой** таблицы + совпадения справа:

```sql
SELECT g.name, s.last_name
FROM s_group g
LEFT JOIN student_in_group sig ON sig.group_id = g.group_id
LEFT JOIN student s ON s.student_id = sig.student_id
ORDER BY g.name, s.last_name;
```

Группы без студентов: `s.last_name IS NULL`.

#### RIGHT OUTER JOIN

Зеркально LEFT — все строки справа:

```sql
SELECT s.last_name, g.name
FROM student_in_group sig
RIGHT JOIN s_group g ON g.group_id = sig.group_id
RIGHT JOIN student s ON s.student_id = sig.student_id;
```

На практике чаще переписывают как LEFT, меняя порядок таблиц.

#### FULL OUTER JOIN

Объединяет LEFT и RIGHT — строки без пары с обеих сторон:

```sql
SELECT s.last_name, g.name
FROM student s
FULL OUTER JOIN student_in_group sig ON sig.student_id = s.student_id
FULL OUTER JOIN s_group g ON g.group_id = sig.group_id;
```

#### Обработка NULL

При OUTER JOIN отсутствующие столбцы — `NULL`. Фильтрация:

```sql
WHERE s.student_id IS NULL   -- только «сироты» справа
```

**Ловушка:** `WHERE s.last_name = 'Иванов'` отфильтрует NULL-строки! Для сохранения используйте условие в `ON`:

```sql
LEFT JOIN student s ON s.student_id = sig.student_id AND s.last_name = 'Иванов'
```

#### Когда использовать

- Отчёт «все группы и число студентов» → LEFT JOIN + COUNT.
- Сравнение двух списков → FULL OUTER JOIN.
"""

THEORY["p3-l13-cross-self-join"] = """### Краткая теория

#### CROSS JOIN — декартово произведение

Каждая строка первой таблицы соединяется с **каждой** строкой второй:

```sql
SELECT s.last_name, g.name
FROM student s
CROSS JOIN s_group g;
```

Если в `student` 100 строк и в `s_group` 20 — результат 2000 строк.

**Риск:** случайный CROSS JOIN без условия в старом синтаксисе (`FROM a, b` без WHERE) создаёт огромный результат.

Полезные применения:
- Генерация комбинаций (расписание × аудитории).
- Явное декартово произведение с последующей фильтрацией.

#### SELF JOIN — самосоединение

Таблица соединяется **с самой собой** через алиасы:

```sql
-- пары студентов с одной фамилией
SELECT a.last_name, a.first_name AS first1, b.first_name AS first2
FROM student a
JOIN student b ON a.last_name = b.last_name AND a.student_id < b.student_id;
```

Условие `a.student_id < b.student_id` исключает дубликаты и пару (A,A).

#### Иерархии (руководитель — подчинённый)

```sql
CREATE TABLE employee (
    emp_id INT PRIMARY KEY,
    name VARCHAR(50),
    manager_id INT REFERENCES employee(emp_id)
);

SELECT e.name AS employee, m.name AS manager
FROM employee e
LEFT JOIN employee m ON e.manager_id = m.emp_id;
```

#### CROSS JOIN vs INNER JOIN

`INNER JOIN ... ON TRUE` эквивалентен `CROSS JOIN`.
"""

THEORY["p3-l14-group-by"] = """### Краткая теория

**Агрегатные функции** сводят множество строк к одному значению:

| Функция | Назначение |
|---------|------------|
| `COUNT(*)` | Число строк |
| `COUNT(столбец)` | Число не-NULL значений |
| `SUM`, `AVG` | Сумма, среднее |
| `MIN`, `MAX` | Минимум, максимум |

#### GROUP BY

Группировка — «разбить строки на группы и агрегировать каждую»:

```sql
SELECT subj.name, AVG(p.grade)::numeric(4,2) AS avg_grade
FROM performance p
JOIN subject subj ON subj.subject_id = p.subject_id
GROUP BY subj.name;
```

#### Правило GROUP BY

В `SELECT` могут быть:
- столбцы из `GROUP BY`;
- агрегатные функции;
- выражения от них.

**Нельзя:** `SELECT last_name, AVG(grade) ... GROUP BY subject_id` — `last_name` не в GROUP BY (кроме функциональной зависимости в PostgreSQL при PK).

#### Несколько столбцов группировки

```sql
SELECT g.name, subj.name, AVG(p.grade)
FROM performance p
JOIN student_in_group sig ON sig.student_id = p.student_id
JOIN s_group g ON g.group_id = sig.group_id
JOIN subject subj ON subj.subject_id = p.subject_id
GROUP BY g.name, subj.name;
```

#### COUNT(*) vs COUNT(столбец)

```sql
SELECT COUNT(*) FROM student;           -- все строки
SELECT COUNT(email) FROM student;       -- без NULL email
```

Справочник: `course/sql/p3-l17-group-by.sql`.
"""

THEORY["p3-l15-having"] = """### Краткая теория

#### WHERE vs HAVING

| | WHERE | HAVING |
|---|-------|--------|
| Применяется к | Отдельным строкам | Группам |
| Момент фильтрации | До группировки | После GROUP BY |
| Агрегаты | Нельзя (обычно) | Можно |

```sql
SELECT g.name, AVG(p.grade) AS avg_grade
FROM s_group g
JOIN student_in_group sig ON sig.group_id = g.group_id
JOIN performance p ON p.student_id = sig.student_id
WHERE g.course_num = 3              -- фильтр строк до группировки
GROUP BY g.name
HAVING AVG(p.grade) >= 4.0;         -- фильтр групп
```

#### Типичные задачи HAVING

```sql
-- группы с более чем 5 студентами
SELECT g.name, COUNT(sig.student_id) AS cnt
FROM s_group g
JOIN student_in_group sig ON sig.group_id = g.group_id
GROUP BY g.name
HAVING COUNT(sig.student_id) > 5;

-- дисциплины с разбросом оценок
SELECT subj.name, MAX(p.grade) - MIN(p.grade) AS spread
FROM performance p
JOIN subject subj ON subj.subject_id = p.subject_id
GROUP BY subj.name
HAVING MAX(p.grade) - MIN(p.grade) > 2;
```

#### Порядок выполнения

FROM → WHERE → GROUP BY → **HAVING** → SELECT → ORDER BY

#### Частая ошибка

Фильтр по агрегату в WHERE — синтаксическая ошибка:

```sql
-- НЕВЕРНО:
WHERE AVG(grade) > 4

-- ВЕРНО:
HAVING AVG(grade) > 4
```
"""

THEORY["p3-l16-subqueries"] = """### Краткая теория

**Подзапрос** (subquery) — SELECT, вложенный в другой SQL-оператор.

#### Скalarный подзапрос

Возвращает одно значение (одну строку, один столбец):

```sql
SELECT last_name, first_name
FROM student
WHERE student_id = (
    SELECT student_id FROM student WHERE email = 'ivanov@uni.local'
);

SELECT last_name, grade
FROM performance p
JOIN student s ON s.student_id = p.student_id
WHERE grade > (SELECT AVG(grade) FROM performance);
```

#### Подзапрос с IN

```sql
SELECT last_name FROM student
WHERE student_id IN (
    SELECT student_id FROM student_in_group WHERE group_id = 1
);
```

> **Осторожно с NOT IN и NULL:** если подзапрос возвращает NULL, результат может быть пустым. Предпочитайте `NOT EXISTS`.

#### EXISTS

Проверка наличия строк (коррелированный подзапрос):

```sql
SELECT name FROM subject subj
WHERE EXISTS (
    SELECT 1 FROM performance p
    WHERE p.subject_id = subj.subject_id
);
```

`EXISTS` останавливается на первом совпадении — часто эффективнее IN.

#### Подзапрос во FROM (производная таблица)

```sql
SELECT g.name, t.avg_grade
FROM s_group g
JOIN (
    SELECT sig.group_id, AVG(p.grade) AS avg_grade
    FROM student_in_group sig
    JOIN performance p ON p.student_id = sig.student_id
    GROUP BY sig.group_id
) t ON t.group_id = g.group_id;
```

#### Подзапрос vs JOIN

Многие запросы записываются обоими способами. JOIN обычно прозрачнее; EXISTS удобен для проверки существования.

Справочник: `course/sql/p3-l19-subqueries.sql`.
"""

THEORY["p3-l17-set-ops"] = """### Краткая теория

**Операции над множествами** объединяют результаты двух SELECT-запросов с **совместимыми** столбцами (число и типы).

#### UNION — объединение

```sql
SELECT last_name, first_name FROM student
UNION
SELECT last_name, first_name FROM student_archive;
```

`UNION` удаляет дубликаты. `UNION ALL` сохраняет все строки (быстрее):

```sql
SELECT email FROM student WHERE email IS NOT NULL
UNION ALL
SELECT email FROM teacher WHERE email IS NOT NULL;
```

#### INTERSECT — пересечение

```sql
SELECT student_id FROM student_in_group WHERE group_id = 1
INTERSECT
SELECT student_id FROM performance WHERE grade = 5;
-- студенты группы 1 с отличной оценкой
```

#### EXCEPT — разность

```sql
SELECT student_id FROM student
EXCEPT
SELECT student_id FROM performance;
-- студенты без оценок
```

#### Требования совместимости

- Одинаковое число столбцов.
- Совместимые типы (PostgreSQL приведёт к общему типу).
- Имена столбцов берутся из **первого** запроса.
- ORDER BY применяется к результату целиком:

```sql
(SELECT ... ) UNION (SELECT ... ) ORDER BY 1;
```

#### Связь с теорией

`UNION`, `INTERSECT`, `EXCEPT` — аналоги операций ∪, ∩, − реляционной алгебры.
"""

THEORY["p3-l18-scalar-funcs"] = """### Краткая теория

**Скalarные функции** возвращают одно значение для каждой строки (или для всего выражения).

#### Строковые функции

```sql
SELECT UPPER(last_name), LOWER(first_name),
       LENGTH(last_name), TRIM(email),
       SUBSTRING(last_name FROM 1 FOR 3),
       CONCAT(last_name, ' ', first_name) AS fio
FROM student;
```

PostgreSQL: `||` — конкатенация; `CONCAT` обрабатывает NULL.

#### Числовые функции

```sql
SELECT ROUND(AVG(grade)::numeric, 2),
       CEIL(hours / 36.0),
       ABS(grade - 3),
       MOD(student_id, 2)
FROM performance;
```

#### Дата и время

```sql
SELECT NOW(), CURRENT_DATE,
       EXTRACT(YEAR FROM birth_date) AS y,
       AGE(birth_date) AS years_old,
       birth_date + INTERVAL '1 year'
FROM student;
```

#### COALESCE и NULLIF

```sql
SELECT COALESCE(email, 'нет почты') FROM student;

SELECT NULLIF(grade, 0)   -- NULL если grade = 0, иначе grade
FROM performance;
```

`COALESCE(a, b, c)` — первый не-NULL аргумент.

#### Функции в WHERE и GROUP BY

```sql
WHERE EXTRACT(YEAR FROM birth_date) = 2004
GROUP BY DATE_TRUNC('month', grade_date)
```
"""

THEORY["p3-l19-case-when"] = """### Краткая теория

#### CASE — условное выражение

```sql
SELECT last_name, grade,
    CASE
        WHEN grade = 5 THEN 'отлично'
        WHEN grade = 4 THEN 'хорошо'
        WHEN grade = 3 THEN 'удовлетворительно'
        ELSE 'неуд'
    END AS rating_text
FROM performance p
JOIN student s ON s.student_id = p.student_id;
```

Простая форма (по значению):

```sql
CASE grade WHEN 5 THEN 'A' WHEN 4 THEN 'B' ELSE 'C' END
```

#### CAST и оператор ::

Приведение типов:

```sql
SELECT AVG(grade)::numeric(4,2);
SELECT CAST(birth_date AS TIMESTAMP);
SELECT '2024-01-15'::DATE;
```

#### Вычисляемые столбцы

```sql
SELECT last_name,
       EXTRACT(YEAR FROM AGE(birth_date)) AS age,
       CASE WHEN email IS NULL THEN FALSE ELSE TRUE END AS has_email
FROM student;
```

#### CASE в агрегатах

```sql
SELECT COUNT(CASE WHEN grade = 5 THEN 1 END) AS fives,
       COUNT(CASE WHEN grade < 4 THEN 1 END) AS poor
FROM performance;
```

Аналог `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`.

#### CASE vs COALESCE

`COALESCE` — частный случай для NULL; `CASE` — произвольная логика.
"""

THEORY["p3-l20-transactions"] = """### Краткая теория

**Транзакция** — логическая единица работы: набор операций выполняется **атомарно**.

#### Управление транзакциями

```sql
BEGIN;   -- или START TRANSACTION;

UPDATE account SET balance = balance - 1000 WHERE id = 1;
UPDATE account SET balance = balance + 1000 WHERE id = 2;

COMMIT;   -- зафиксировать
-- ROLLBACK;  -- откатить
```

В **psql** каждая команда без явного BEGIN выполняется в autocommit-режиме.

#### ACID

| Свойство | Смысл |
|----------|-------|
| **A**tomicity | Всё или ничего |
| **C**onsistency | БД остаётся в согласованном состоянии |
| **I**solation | Транзакции не меша друг другу (уровни изоляции) |
| **D**urability | Зафиксированные данные сохраняются после сбоя |

#### SAVEPOINT

```sql
BEGIN;
INSERT INTO student (last_name, first_name, birth_date)
VALUES ('Тест', 'Тест', '2000-01-01');
SAVEPOINT sp1;
DELETE FROM student WHERE last_name = 'Тест';
ROLLBACK TO sp1;   -- отменить DELETE, INSERT остаётся
COMMIT;
```

#### Ошибки и откат

При ошибке в транзакции PostgreSQL переводит её в состояние **aborted** — нужен `ROLLBACK` перед новыми командами.

#### Практический пример: перевод студента

```sql
BEGIN;
UPDATE student_in_group SET group_id = 2
WHERE student_id = 1 AND group_id = 1;
INSERT INTO audit_log (action, ts) VALUES ('transfer', NOW());
COMMIT;
```
"""

THEORY["p3-l21-isolation"] = """### Краткая теория

При **параллельном** выполнении транзакций без изоляции возможны **анomalies**.

#### Аномалии

| Аномалия | Описание |
|----------|----------|
| Dirty read | Чтение незафиксированных данных другой транзакции |
| Non-repeatable read | Повторное чтение — другое значение |
| Phantom read | Появление новых строк при повторном запросе |
| Serialization anomaly | Результат не эквивалентен никакому последовательному порядку |

#### Уровни изоляции в PostgreSQL

```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;   -- по умолчанию
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

| Уровень | Dirty read | Non-repeatable | Phantom |
|---------|------------|----------------|---------|
| READ UNCOMMITTED | — (PG как RC) | — | — |
| READ COMMITTED | Нет | Да | Да |
| REPEATABLE READ | Нет | Нет | Нет* |
| SERIALIZABLE | Нет | Нет | Нет |

*В PostgreSQL REPEATABLE READ использует snapshot и блокирует phantom для большинства случаев.

#### Пример REPEATABLE READ

```sql
-- Сессия 1
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT AVG(grade) FROM performance;  -- 4.2
-- Сессия 2: INSERT новой оценки; COMMIT;
SELECT AVG(grade) FROM performance;  -- всё ещё 4.2
COMMIT;
```

#### Выбор уровня

- OLTP по умолчанию: **READ COMMITTED**.
- Отчёты с согласованным снимком: **REPEATABLE READ**.
- Критичные финансовые операции: **SERIALIZABLE** (возможны откаты serialization failure).
"""

THEORY["p3-l22-views"] = """### Краткая теория

**Представление** (VIEW) — сохранённый запрос SELECT, используемый как виртуальная таблица.

#### Создание VIEW

```sql
CREATE VIEW v_student_groups AS
SELECT s.student_id, s.last_name, s.first_name, g.name AS group_name
FROM student s
JOIN student_in_group sig ON sig.student_id = s.student_id
JOIN s_group g ON g.group_id = sig.group_id;

SELECT * FROM v_student_groups WHERE group_name = 'ИВТ-21';
```

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
"""

THEORY["p3-l23-triggers"] = """### Краткая теория

**Триггер** — функция, автоматически вызываемая при INSERT/UPDATE/DELETE (или TRUNCATE).

#### Функция PL/pgSQL

```sql
CREATE OR REPLACE FUNCTION audit_student_change()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO student_audit (student_id, action, changed_at)
    VALUES (COALESCE(NEW.student_id, OLD.student_id), TG_OP, NOW());
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;
```

#### Создание триггера

```sql
CREATE TRIGGER trg_student_audit
AFTER INSERT OR UPDATE OR DELETE ON student
FOR EACH ROW EXECUTE FUNCTION audit_student_change();
```

| Параметр | Значения |
|----------|----------|
| Момент | `BEFORE`, `AFTER`, `INSTEAD OF` |
| Гранулярность | `FOR EACH ROW`, `FOR EACH STATEMENT` |
| Событие | `INSERT`, `UPDATE`, `DELETE` |

#### BEFORE vs AFTER

- **BEFORE** — может изменить NEW или отменить операцию (`RETURN NULL`).
- **AFTER** — логирование, каскадная логика (FK уже проверен).

#### NEW и OLD

- INSERT: только `NEW`.
- DELETE: только `OLD`.
- UPDATE: оба.

#### Практика аудита

Триггеры удобны для журналирования, но усложняют отладку и тестирование. Для сложной логики рассматривайте приложение или logical replication.
"""

THEORY["p3-l24-exam"] = """### Краткая теория (повторение Part 3)

Итоговый контроль охватывает **главы 3–11 Morgunov** и **задания 4–7 практикума**.

#### Контрольный чек-лист

**DDL**
- [ ] CREATE TABLE со схемой, типами, PK/FK/CHECK
- [ ] ALTER TABLE: столбцы, типы, ограничения

**DML**
- [ ] INSERT (многострочный, RETURNING, SELECT)
- [ ] UPDATE с WHERE и FROM
- [ ] DELETE vs TRUNCATE, CASCADE

**SELECT**
- [ ] WHERE, ORDER BY, DISTINCT, LIMIT
- [ ] INNER / LEFT / FULL JOIN
- [ ] GROUP BY, HAVING, агрегаты
- [ ] Подзапросы: scalar, IN, EXISTS
- [ ] UNION / INTERSECT / EXCEPT

**Продвинутое**
- [ ] Скalarные функции, CASE, CAST
- [ ] Транзакции, уровни изоляции
- [ ] VIEW, триггеры (базово)

#### Типовые ошибки на экзамене

1. `WHERE column = NULL` вместо `IS NULL`.
2. Столбцы в SELECT не входят в GROUP BY.
3. UPDATE/DELETE без WHERE.
4. NOT IN с NULL в подзапросе.
5. Путаница HAVING и WHERE.

#### Подготовка

1. Разверните схему: `\\i course/sql/schema-university.sql`
2. Загрузите данные: `\\i course/sql/p3-l22-lab-university.sql`
3. Решите задачи из каждого `.tasks.md` Part 3 без подсказок.
4. Пройдите все quiz с результатом ≥ 70%.
"""

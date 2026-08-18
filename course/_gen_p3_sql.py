# -*- coding: utf-8 -*-

SCHEMA_UNIVERSITY = """-- schema-university.sql
-- Базовая схема «Университет» для лабораторных работ Part 3
-- PostgreSQL, UTF-8

DROP SCHEMA IF EXISTS university CASCADE;
CREATE SCHEMA university;
SET search_path TO university, public;

-- Факультет
CREATE TABLE faculty (
    faculty_id   SERIAL PRIMARY KEY,
    name         VARCHAR(100) NOT NULL UNIQUE,
    short_name   VARCHAR(20)
);

-- Группа (s_group — имя из практикума Morgunov)
CREATE TABLE s_group (
    group_id     SERIAL PRIMARY KEY,
    name         VARCHAR(20) NOT NULL UNIQUE,
    faculty_id   INT NOT NULL REFERENCES faculty(faculty_id),
    course_num   SMALLINT NOT NULL CHECK (course_num BETWEEN 1 AND 6),
    entry_year   INT NOT NULL
);

-- Студент
CREATE TABLE student (
    student_id   SERIAL PRIMARY KEY,
    last_name    VARCHAR(50) NOT NULL,
    first_name   VARCHAR(50) NOT NULL,
    middle_name  VARCHAR(50),
    birth_date   DATE NOT NULL,
    email        VARCHAR(100) UNIQUE
);

-- Связь студент — группа (многие-ко-многим с историей)
CREATE TABLE student_in_group (
    student_id   INT NOT NULL REFERENCES student(student_id) ON DELETE CASCADE,
    group_id     INT NOT NULL REFERENCES s_group(group_id) ON DELETE CASCADE,
    enrolled_at  DATE NOT NULL DEFAULT CURRENT_DATE,
    PRIMARY KEY (student_id, group_id)
);

-- Преподаватель
CREATE TABLE teacher (
    teacher_id   SERIAL PRIMARY KEY,
    last_name    VARCHAR(50) NOT NULL,
    first_name   VARCHAR(50) NOT NULL,
    degree       VARCHAR(30)
);

-- Дисциплина
CREATE TABLE subject (
    subject_id   SERIAL PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    hours        SMALLINT NOT NULL CHECK (hours > 0)
);

-- Успеваемость (оценки)
CREATE TABLE performance (
    perf_id      SERIAL PRIMARY KEY,
    student_id   INT NOT NULL REFERENCES student(student_id),
    subject_id   INT NOT NULL REFERENCES subject(subject_id),
    teacher_id   INT NOT NULL REFERENCES teacher(teacher_id),
    grade_date   DATE NOT NULL DEFAULT CURRENT_DATE,
    grade        SMALLINT NOT NULL CHECK (grade BETWEEN 2 AND 5),
    UNIQUE (student_id, subject_id, grade_date)
);

COMMENT ON SCHEMA university IS 'Учебная БД курса «Базы данных»';
"""

SQL_CREATE_TABLES = """-- p3-l01-create-tables.sql
-- CREATE TABLE: студент, группа, связь студент-группа

CREATE SCHEMA IF NOT EXISTS lab;
SET search_path TO lab, public;

CREATE TABLE IF NOT EXISTS student (
    student_id   SERIAL PRIMARY KEY,
    last_name    VARCHAR(50) NOT NULL,
    first_name   VARCHAR(50) NOT NULL,
    birth_date   DATE NOT NULL
);

COMMENT ON TABLE student IS 'Студенты университета';

CREATE TABLE IF NOT EXISTS s_group (
    group_id     SERIAL PRIMARY KEY,
    name         VARCHAR(20) NOT NULL UNIQUE,
    course_num   SMALLINT NOT NULL
);

CREATE TABLE IF NOT EXISTS student_in_group (
    student_id   INT NOT NULL REFERENCES student(student_id),
    group_id     INT NOT NULL REFERENCES s_group(group_id),
    enrolled_at  DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (student_id, group_id)
);
"""

SQL_INSERT_SELECT = """-- p3-l02-insert-select.sql
-- INSERT и SELECT на схеме university

SET search_path TO university, public;

-- Одна строка
INSERT INTO faculty (name, short_name)
VALUES ('Факультет информатики', 'ФИ')
RETURNING faculty_id, name;

-- Несколько строк
INSERT INTO s_group (name, faculty_id, course_num, entry_year) VALUES
    ('ИВТ-21', 1, 3, 2021),
    ('ИВТ-22', 1, 2, 2022),
    ('ПМИ-21', 1, 3, 2021);

INSERT INTO student (last_name, first_name, birth_date, email) VALUES
    ('Иванов', 'Пётр', '2003-05-12', 'ivanov@uni.local'),
    ('Петрова', 'Анна', '2004-01-20', 'petrova@uni.local');

INSERT INTO student_in_group (student_id, group_id)
SELECT s.student_id, g.group_id
FROM student s, s_group g
WHERE s.last_name = 'Иванов' AND g.name = 'ИВТ-21';

-- Базовый SELECT
SELECT student_id, last_name, first_name
FROM student
ORDER BY last_name;

SELECT s.last_name, g.name AS group_name
FROM student s
JOIN student_in_group sig ON sig.student_id = s.student_id
JOIN s_group g ON g.group_id = sig.group_id;
"""

SQL_DATA_TYPES = """-- p3-l04-data-types.sql
-- Примеры типов данных PostgreSQL

CREATE SCHEMA IF NOT EXISTS types_demo;
SET search_path TO types_demo;

CREATE TABLE type_samples (
    id              SERIAL PRIMARY KEY,
    code_int        INTEGER,
    code_big        BIGINT,
    amount          NUMERIC(10, 2),
    ratio           REAL,
    flag            BOOLEAN DEFAULT FALSE,
    note_short      VARCHAR(50),
    note_long       TEXT,
    created_at      TIMESTAMP DEFAULT NOW(),
    event_date      DATE,
    duration        INTERVAL,
    tags            TEXT[],
    meta            JSONB
);

INSERT INTO type_samples (code_int, amount, flag, note_short, event_date, duration, tags, meta)
VALUES (
    42,
    1999.99,
    TRUE,
    'Пример',
    '2024-09-01',
    '2 hours 30 minutes',
    ARRAY['sql', 'postgres'],
    '{"level": "beginner"}'::jsonb
);

SELECT pg_typeof(code_int), pg_typeof(amount), pg_typeof(meta) FROM type_samples;
"""

SQL_CONSTRAINTS = """-- p3-l06-ddl-constraints.sql
-- PRIMARY KEY, FOREIGN KEY, CHECK, UNIQUE

CREATE SCHEMA IF NOT EXISTS constr_demo;
SET search_path TO constr_demo;

CREATE TABLE department (
    dept_id   SERIAL PRIMARY KEY,
    name      VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE employee (
    emp_id       SERIAL PRIMARY KEY,
    dept_id      INT NOT NULL REFERENCES department(dept_id)
                 ON UPDATE CASCADE ON DELETE RESTRICT,
    full_name    VARCHAR(100) NOT NULL,
    salary       NUMERIC(12,2) NOT NULL CHECK (salary > 0),
    email        VARCHAR(100) UNIQUE,
    hire_date    DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Составной первичный ключ
CREATE TABLE project_member (
    project_code VARCHAR(20) NOT NULL,
    emp_id       INT NOT NULL REFERENCES employee(emp_id) ON DELETE CASCADE,
    role         VARCHAR(30) NOT NULL,
    PRIMARY KEY (project_code, emp_id)
);
"""

SQL_JOINS = """-- p3-l14-joins.sql
-- INNER JOIN: студенты и группы

SET search_path TO university, public;

-- Две таблицы
SELECT s.last_name, s.first_name, g.name AS group_name, g.course_num
FROM student s
INNER JOIN student_in_group sig ON sig.student_id = s.student_id
INNER JOIN s_group g ON g.group_id = sig.group_id
WHERE g.course_num = 3
ORDER BY g.name, s.last_name;

-- Три таблицы: оценки
SELECT s.last_name, subj.name AS subject, p.grade, p.grade_date
FROM performance p
JOIN student s ON s.student_id = p.student_id
JOIN subject subj ON subj.subject_id = p.subject_id
WHERE p.grade >= 4;

-- Эквивалент через WHERE (устаревший стиль)
SELECT s.last_name, g.name
FROM student s, student_in_group sig, s_group g
WHERE sig.student_id = s.student_id AND g.group_id = sig.group_id;
"""

SQL_GROUP_BY = """-- p3-l17-group-by.sql
-- GROUP BY и агрегатные функции

SET search_path TO university, public;

-- Средний балл по дисциплинам
SELECT subj.name,
       COUNT(*) AS grades_count,
       ROUND(AVG(p.grade)::numeric, 2) AS avg_grade,
       MIN(p.grade) AS min_grade,
       MAX(p.grade) AS max_grade
FROM performance p
JOIN subject subj ON subj.subject_id = p.subject_id
GROUP BY subj.name
ORDER BY avg_grade DESC;

-- Количество студентов в каждой группе
SELECT g.name, COUNT(sig.student_id) AS students_cnt
FROM s_group g
LEFT JOIN student_in_group sig ON sig.group_id = g.group_id
GROUP BY g.group_id, g.name
HAVING COUNT(sig.student_id) > 0;
"""

SQL_SUBQUERIES = """-- p3-l19-subqueries.sql
-- Скalar, IN, EXISTS

SET search_path TO university, public;

-- Скalar: средний балл для сравнения
SELECT s.last_name, subj.name, p.grade
FROM performance p
JOIN student s ON s.student_id = p.student_id
JOIN subject subj ON subj.subject_id = p.subject_id
WHERE p.grade > (
    SELECT AVG(grade) FROM performance
);

-- IN: студенты из группы ИВТ-21
SELECT last_name, first_name
FROM student
WHERE student_id IN (
    SELECT sig.student_id
    FROM student_in_group sig
    JOIN s_group g ON g.group_id = sig.group_id
    WHERE g.name = 'ИВТ-21'
);

-- EXISTS: дисциплины, по которым есть оценки
SELECT name FROM subject subj
WHERE EXISTS (
    SELECT 1 FROM performance p WHERE p.subject_id = subj.subject_id
);

-- Подзапрос во FROM
SELECT g.name, stats.avg_grade
FROM s_group g
JOIN (
    SELECT sig.group_id, AVG(p.grade) AS avg_grade
    FROM student_in_group sig
    JOIN performance p ON p.student_id = sig.student_id
    GROUP BY sig.group_id
) stats ON stats.group_id = g.group_id;
"""

SQL_LAB_UNIVERSITY = """-- p3-l22-lab-university.sql
-- Полная лабораторная схема «Университет» + тестовые данные
-- Выполните после schema-university.sql или самостоятельно

\\i schema-university.sql

SET search_path TO university, public;

INSERT INTO faculty (name, short_name) VALUES
    ('Факультет информатики', 'ФИ'),
    ('Факультет математики', 'ФМ');

INSERT INTO s_group (name, faculty_id, course_num, entry_year) VALUES
    ('ИВТ-21', 1, 3, 2021),
    ('ИВТ-22', 1, 2, 2022),
    ('ПМИ-21', 2, 3, 2021);

INSERT INTO student (last_name, first_name, middle_name, birth_date, email) VALUES
    ('Иванов', 'Пётр', 'Сергеевич', '2003-05-12', 'ivanov@uni.local'),
    ('Петрова', 'Анна', 'Игоревна', '2004-01-20', 'petrova@uni.local'),
    ('Сидоров', 'Олег', NULL, '2003-11-03', 'sidorov@uni.local'),
    ('Козлова', 'Мария', 'Андреевна', '2004-07-15', NULL);

INSERT INTO student_in_group (student_id, group_id) VALUES
    (1, 1), (2, 1), (3, 2), (4, 3);

INSERT INTO teacher (last_name, first_name, degree) VALUES
    ('Смирнов', 'Алексей', 'доцент'),
    ('Кузнецова', 'Елена', 'профессор');

INSERT INTO subject (name, hours) VALUES
    ('Базы данных', 72),
    ('Алгоритмы', 108),
    ('Математический анализ', 144);

INSERT INTO performance (student_id, subject_id, teacher_id, grade_date, grade) VALUES
    (1, 1, 1, '2024-01-15', 5),
    (1, 2, 1, '2024-02-01', 4),
    (2, 1, 1, '2024-01-15', 5),
    (2, 3, 2, '2024-03-10', 4),
    (3, 1, 1, '2024-01-15', 3),
    (4, 3, 2, '2024-03-10', 5);

-- Контрольные запросы
SELECT g.name, COUNT(DISTINCT sig.student_id) AS cnt
FROM s_group g
LEFT JOIN student_in_group sig ON sig.group_id = g.group_id
GROUP BY g.name;

SELECT s.last_name, AVG(p.grade)::numeric(4,2) AS avg_grade
FROM student s
JOIN performance p ON p.student_id = s.student_id
GROUP BY s.student_id, s.last_name
HAVING AVG(p.grade) >= 4.5;
"""

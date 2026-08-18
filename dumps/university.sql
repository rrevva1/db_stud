-- dumps/university.sql
-- Схема «Университет» + тестовые данные для курса db_stud
-- PostgreSQL, UTF-8. Самодостаточный скрипт (без \i).

DROP SCHEMA IF EXISTS university CASCADE;
CREATE SCHEMA university;
SET search_path TO university, public;

CREATE TABLE faculty (
    faculty_id   SERIAL PRIMARY KEY,
    name         VARCHAR(100) NOT NULL UNIQUE,
    short_name   VARCHAR(20)
);

CREATE TABLE s_group (
    group_id     SERIAL PRIMARY KEY,
    name         VARCHAR(20) NOT NULL UNIQUE,
    faculty_id   INT NOT NULL REFERENCES faculty(faculty_id),
    course_num   SMALLINT NOT NULL CHECK (course_num BETWEEN 1 AND 6),
    entry_year   INT NOT NULL
);

CREATE TABLE student (
    student_id   SERIAL PRIMARY KEY,
    last_name    VARCHAR(50) NOT NULL,
    first_name   VARCHAR(50) NOT NULL,
    middle_name  VARCHAR(50),
    birth_date   DATE NOT NULL,
    email        VARCHAR(100) UNIQUE
);

CREATE TABLE student_in_group (
    student_id   INT NOT NULL REFERENCES student(student_id) ON DELETE CASCADE,
    group_id     INT NOT NULL REFERENCES s_group(group_id) ON DELETE CASCADE,
    enrolled_at  DATE NOT NULL DEFAULT CURRENT_DATE,
    PRIMARY KEY (student_id, group_id)
);

CREATE TABLE teacher (
    teacher_id   SERIAL PRIMARY KEY,
    last_name    VARCHAR(50) NOT NULL,
    first_name   VARCHAR(50) NOT NULL,
    degree       VARCHAR(30)
);

CREATE TABLE subject (
    subject_id   SERIAL PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    hours        SMALLINT NOT NULL CHECK (hours > 0)
);

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

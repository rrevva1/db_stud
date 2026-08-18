-- schema-university.sql
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

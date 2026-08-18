-- p3-l01-create-tables.sql
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

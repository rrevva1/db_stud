-- p3-l06-ddl-constraints.sql
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

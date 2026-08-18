-- p5-l01-indexes-btree.sql
-- Демонстрация B-tree индексов в PostgreSQL (UTF-8)
-- Запуск: psql -f course/sql/p5-l01-indexes-btree.sql

DROP TABLE IF EXISTS idx_demo_employee CASCADE;

CREATE TABLE idx_demo_employee (
    id          SERIAL PRIMARY KEY,
    email       TEXT NOT NULL,
    department  TEXT NOT NULL,
    salary      NUMERIC(10,2) NOT NULL,
    hired_at    DATE DEFAULT CURRENT_DATE
);

-- Наполнение тестовыми данными
INSERT INTO idx_demo_employee (email, department, salary)
SELECT
    'user' || g || '@uni.ru',
    (ARRAY['IT','HR','Sales','Ops'])[1 + (g % 4)],
    30000 + (random() * 70000)::numeric(10,2)
FROM generate_series(1, 50000) AS g;

ANALYZE idx_demo_employee;

-- 1. Seq Scan без индекса на email
EXPLAIN (COSTS OFF)
SELECT * FROM idx_demo_employee WHERE email = 'user12345@uni.ru';

-- 2. Создание B-tree индекса
CREATE INDEX idx_demo_employee_email ON idx_demo_employee (email);

EXPLAIN (COSTS OFF)
SELECT * FROM idx_demo_employee WHERE email = 'user12345@uni.ru';

-- 3. Составной индекс для фильтра + сортировки
CREATE INDEX idx_demo_dept_salary ON idx_demo_employee (department, salary DESC);

EXPLAIN (COSTS OFF)
SELECT * FROM idx_demo_employee
WHERE department = 'IT'
ORDER BY salary DESC
LIMIT 10;

-- 4. Индекс на выражение (case-insensitive поиск)
CREATE INDEX idx_demo_email_lower ON idx_demo_employee (lower(email));

EXPLAIN (COSTS OFF)
SELECT * FROM idx_demo_employee WHERE lower(email) = 'user999@uni.ru';

-- 5. UNIQUE индекс
CREATE UNIQUE INDEX idx_demo_email_unique ON idx_demo_employee (email);

-- Просмотр индексов
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'idx_demo_employee';

-- Очистка (опционально)
-- DROP TABLE idx_demo_employee CASCADE;

-- p5-l04-transactions-acid.sql
-- Транзакции и свойства ACID в PostgreSQL (UTF-8)
-- Дополнительная практика к теме надёжности (связь с частью 3, углубление в части 5)

DROP TABLE IF EXISTS acid_account CASCADE;

CREATE TABLE acid_account (
    id      SERIAL PRIMARY KEY,
    name    TEXT NOT NULL,
    balance NUMERIC(12,2) NOT NULL CHECK (balance >= 0)
);

INSERT INTO acid_account (name, balance) VALUES
    ('Alice', 1000.00),
    ('Bob',   1000.00);

-- A — Atomicity: перевод либо полностью, либо откат
BEGIN;
    UPDATE acid_account SET balance = balance - 200 WHERE name = 'Alice';
    UPDATE acid_account SET balance = balance + 200 WHERE name = 'Bob';
    -- ROLLBACK;  -- раскомментируйте для проверки отката
COMMIT;

SELECT * FROM acid_account;

-- C — Consistency: CHECK balance >= 0
BEGIN;
    UPDATE acid_account SET balance = balance - 5000 WHERE name = 'Alice';
    UPDATE acid_account SET balance = balance + 5000 WHERE name = 'Bob';
COMMIT;  -- ошибка: нарушение CHECK на Alice

-- I — Isolation (демо dirty read не виден в READ COMMITTED)
-- Сессия 1:
BEGIN;
UPDATE acid_account SET balance = balance - 100 WHERE name = 'Alice';
-- не COMMIT — в другой сессии SELECT покажет старое значение (READ COMMITTED)

-- D — Durability: после COMMIT данные переживут сбой (WAL)
BEGIN;
UPDATE acid_account SET balance = balance + 50 WHERE name = 'Bob';
COMMIT;

-- SAVEPOINT
BEGIN;
    UPDATE acid_account SET balance = balance - 10 WHERE name = 'Alice';
    SAVEPOINT sp1;
    UPDATE acid_account SET balance = balance - 9999 WHERE name = 'Alice';  -- может упасть
    ROLLBACK TO SAVEPOINT sp1;
COMMIT;

-- Уровень изоляции
SHOW transaction_isolation;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN;
SELECT sum(balance) FROM acid_account;
-- повторный SELECT в той же транзакции — тот же снимок
COMMIT;

SELECT * FROM acid_account;

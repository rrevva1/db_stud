-- p3-l04-data-types.sql
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

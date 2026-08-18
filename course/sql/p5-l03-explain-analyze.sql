-- p5-l03-explain-analyze.sql
-- EXPLAIN ANALYZE: сравнение планов с разными типами индексов (UTF-8)

DROP TABLE IF EXISTS explain_demo_log CASCADE;

CREATE TABLE explain_demo_log (
    id         BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    user_id    INT NOT NULL,
    payload    JSONB,
    tags       TEXT[]
);

INSERT INTO explain_demo_log (created_at, user_id, payload, tags)
SELECT
    now() - (g || ' seconds')::interval,
    (random() * 1000)::int,
    jsonb_build_object('action', (ARRAY['login','view','buy'])[1 + (g % 3)], 'ok', true),
    ARRAY(SELECT (ARRAY['web','mobile','api'])[1 + (random()*2)::int])
FROM generate_series(1, 200000) AS g;

ANALYZE explain_demo_log;

-- Без индекса: фильтр по времени
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT count(*) FROM explain_demo_log
WHERE created_at > now() - interval '1 hour';

-- B-tree на created_at
CREATE INDEX idx_explain_demo_created ON explain_demo_log (created_at);

EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*) FROM explain_demo_log
WHERE created_at > now() - interval '1 hour';

-- BRIN (компактный для временных рядов)
DROP INDEX idx_explain_demo_created;
CREATE INDEX idx_explain_demo_brin ON explain_demo_log USING brin (created_at);

EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*) FROM explain_demo_log
WHERE created_at > now() - interval '1 hour';

-- GIN на jsonb
CREATE INDEX idx_explain_demo_gin ON explain_demo_log USING gin (payload jsonb_path_ops);

EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*) FROM explain_demo_log
WHERE payload @> '{"action":"buy"}';

-- Размеры индексов
SELECT
    indexrelid::regclass AS index_name,
    pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
WHERE relid = 'explain_demo_log'::regclass;

-- Чтение ключевых полей плана:
-- Seq Scan vs Index Scan / Bitmap Index Scan
-- actual time, rows, loops
-- Buffers: shared hit/read

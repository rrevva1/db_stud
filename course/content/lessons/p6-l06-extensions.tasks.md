## Практика PostgreSQL

1. `SELECT name, default_version FROM pg_available_extensions ORDER BY name LIMIT 20;`
2. CREATE EXTENSION pg_trgm; — similarity('student','students').
3. FTS: to_tsvector/to_tsquery по русскому тексту.
4. Сохраните: `course/sql/p6-l06-extensions-solution.sql`

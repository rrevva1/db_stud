## Практика PostgreSQL

1. CREATE ROLE app_read NOLOGIN; GRANT SELECT на student, s_group.
2. CREATE USER app1 LOGIN PASSWORD 'test'; GRANT app_read TO app1;
3. Проверьте: app1 может SELECT, не может INSERT.
4. REVOKE и проверка снова.

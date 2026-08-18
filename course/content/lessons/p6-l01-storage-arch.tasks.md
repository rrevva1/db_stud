## Задания

1. Нарисуйте схему: клиент → postmaster → backend → shared_buffers → диск.
2. ```sql
   SELECT datname, blks_hit, blks_read,
          round(100.0*blks_hit/nullif(blks_hit+blks_read,0),2) AS hit_pct
   FROM pg_stat_database WHERE datname=current_database();
   ```
3. Объясните связь shared_buffers и latency SELECT.
4. Прочитайте Morgunov §18.1.

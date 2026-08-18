## Задания

1. Запишите wal_level, max_wal_size, checkpoint_timeout.
2. `SELECT pg_current_wal_lsn(), pg_walfile_name(pg_current_wal_lsn());`
3. Timeline: COMMIT → WAL → checkpoint → data files.
4. Разница minimal vs replica vs logical.

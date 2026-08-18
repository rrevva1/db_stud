## Практика PostgreSQL

### Задание 1. Наблюдение dead tuples

Создайте таблицу, выполните 10 000 UPDATE одних и тех же строк. Проверьте `n_dead_tup` в `pg_stat_user_tables`.

### Задание 2. VACUUM

Запустите `VACUUM VERBOSE` и убедитесь, что `n_dead_tup` уменьшился.

### Задание 3. VACUUM ANALYZE

После массовых изменений — `VACUUM ANALYZE`. Сравните план запроса до/после.

### Задание 4. Настройка autovacuum

Для «горячей» таблицы задайте более агressive `autovacuum_vacuum_scale_factor = 0.02`. Опишите эффект.

### Задание 5. (Осторожно) VACUUM FULL

На **тестовой** копии таблицы выполните VACUUM FULL, сравните `pg_table_size` до/после.

### Самопроверка

- [ ] Понимаете разницу VACUUM и VACUUM FULL
- [ ] Знаете, где смотреть last_autovacuum
- [ ] Не запускаете VACUUM FULL на production без окна

Сохраните: `course/sql/p5-l07-vacuum-solution.sql`

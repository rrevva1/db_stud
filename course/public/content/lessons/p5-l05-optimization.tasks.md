## Практика PostgreSQL

### Задание 1. ANALYZE

Загрузите 100k строк, выполните запрос до ANALYZE и после. Сравните estimated rows в EXPLAIN.

### Задание 2. Рефакторинг

Перепишите `WHERE lower(email) = 'x'` в форму с диапазоном/индексом на `lower(email)` или citext.

### Задание 3. EXISTS vs IN

Один запрос двумя способами: `WHERE id IN (SELECT ...)` и `WHERE EXISTS (SELECT 1 ...)`. Сравните планы и время.

### Задание 4. pg_stat_statements

Если расширение доступно — найдите топ-3 запроса по total_exec_time. Если нет — опишите шаги включения в postgresql.conf.

### Самопроверка

- [ ] После bulk load выполнен ANALYZE
- [ ] План улучшился или объяснено, почему нет
- [ ] Нет регрессии корректности результата

Сохраните: `course/sql/p5-l05-optimization-solution.sql`

## Практика PostgreSQL

### Задание 1. Составной индекс

Таблица `booking(flight_id, passenger_id, booked_at, status)`. Создайте индекс для запроса «бронирования рейса X за период, статус confirmed». Обоснуйте порядок столбцов.

### Задание 2. Partial index

Индекс только на активных студентов (`expelled IS NULL`). Сравните размер индекса с полным через `pg_relation_size`.

### Задание 3. INCLUDE

Индекс на `(student_id) INCLUDE (grade)` для запроса «список оценок студента без обращения к heap» — проверьте Index-Only Scan в EXPLAIN.

### Задание 4. Hash vs B-tree

На столбце равенства создайте hash и btree. Сравните EXPLAIN для `WHERE col = constant`.

### Самопроверка

- [ ] Запрос использует созданный индекс
- [ ] Partial: предикат индекса совпадает с WHERE
- [ ] Порядок столбцов обоснован

Сохраните: `course/sql/p5-l02-btree-hash-solution.sql`

## Практика PostgreSQL

См. также: `course/sql/p5-l06-functions-plpgsql.sql`

### Задание 1. RANGE по месяцам

Секционированная таблица `flight_log(flight_date, ...)` по месяцам 2024. INSERT в разные месяцы, EXPLAIN с фильтром по одному месяцу.

### Задание 2. LIST по регионам

`sales(region, amount)` — секции EU, US, OTHER (DEFAULT partition опционально).

### Задание 3. HASH

4 hash-секции на `booking_id`. Равномерность распределения — `SELECT tableoid::regclass, count(*) ... GROUP BY 1`.

### Задание 4. Архивация

Создайте секцию «старше года», загрузите данные, удалите секцию через `DROP TABLE ... PARTITION OF`.

### Самопроверка

- [ ] EXPLAIN показывает Append только на нужных секциях
- [ ] INSERT попадает в правильную секцию
- [ ] PK/UNIQUE включают ключ секционирования (если задан)

Сохраните: `course/sql/p5-l06-partitioning-solution.sql`

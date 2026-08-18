## Практика PostgreSQL

**Данные:** схема `university` после `schema-university.sql`.

### Задание 1. Один студент

```sql
INSERT INTO student (last_name, first_name, birth_date, email)
VALUES ('Новиков', 'Дмитрий', '2004-03-01', 'novikov@uni.local')
RETURNING student_id;
```

### Задание 2. Пакетная вставка

Добавьте 3 группы и 5 студентов одним `INSERT ... VALUES (...), (...), ...`.

### Задание 3. INSERT ... SELECT

Скопируйте всех студентов группы `ИВТ-21` в таблицу `student_ивт21` (создайте её как `CREATE TABLE ... AS SELECT ...`).

**Справочник:** `course/sql/p3-l02-insert-select.sql`

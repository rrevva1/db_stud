## Практика PostgreSQL

### Задание 1. Ограничения на performance

На схеме `university` добавьте (если нет) `CHECK (grade BETWEEN 2 AND 5)` и `UNIQUE (student_id, subject_id, grade_date)`.

### Задание 2. Нарушение FK

Попробуйте вставить в `student_in_group` несуществующий `student_id`. Зафиксируйте текст ошибки и SQLSTATE.

### Задание 3. CASCADE

Создайте тестовую таблицу с `ON DELETE CASCADE`. Удалите родительскую строку и проверьте дочерние.

**Справочник:** `course/sql/p3-l06-ddl-constraints.sql`

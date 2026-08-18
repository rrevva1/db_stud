## Практика PostgreSQL

### Задание 1. DELETE с WHERE

Удалите тестового студента «Новиков» (если создавали). Используйте `RETURNING`.

### Задание 2. CASCADE

Удалите студента, состоящего в группе. Проверьте, удалилась ли запись в `student_in_group`.

### Задание 3. TRUNCATE

На копии таблицы `performance` выполните `TRUNCATE ... RESTART IDENTITY`. Сравните время/поведение с `DELETE FROM performance`.

### Вопрос для отчёта

Когда предпочтительнее TRUNCATE, а когда DELETE?

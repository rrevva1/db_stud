## Практика PostgreSQL

### Задание 1. Точечное обновление

Обновите email студента с `student_id = 1`. Используйте `RETURNING`.

### Задание 2. UPDATE ... FROM

Повысьте на 1 балл все оценки студентов группы `ИВТ-21`, где оценка = 4 (не выше 5):

```sql
UPDATE performance p
SET grade = grade + 1
FROM student_in_group sig
JOIN s_group g ON g.group_id = sig.group_id
WHERE ...
```

### Задание 3. Безопасность

Сначала выполните `SELECT` с тем же условием, что и UPDATE. Сколько строк будет затронуто?

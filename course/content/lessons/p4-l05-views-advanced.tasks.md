## Практика PostgreSQL

### Задание 1. Обновляемое VIEW

Создайте `active_students` — студенты без поля `expelled`. Выполните `UPDATE` зарплаты стипендии (условное поле) через VIEW.

### Задание 2. WITH CHECK OPTION

VIEW `group_101_students` с фильтром `group_id = 101`. Попробуйте `INSERT` студента в другую группу — зафиксируйте ошибку.

### Задание 3. INSTEAD OF UPDATE

VIEW `student_group_view` с JOIN `student` и `s_group`. Триггер INSTEAD OF для обновления `student.name` и `s_group.name` раздельно.

### Задание 4. Rule (опционально)

Создайте простое VIEW и RULE `ON INSERT DO INSTEAD` в базовую таблицу. Сравните поведение с триггером.

### Самопроверка

- [ ] SELECT через VIEW возвращает ожидаемый подмножество
- [ ] DML через VIEW отражается в базовых таблицах
- [ ] CHECK OPTION блокирует «невидимые» строки

Сохраните: `course/sql/p4-l05-views-advanced-solution.sql`

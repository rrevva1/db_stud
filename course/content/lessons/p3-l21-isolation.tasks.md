## Практика PostgreSQL

**Нужны две сессии psql.**

### Задание 1. READ COMMITTED

Сессия 1: BEGIN; UPDATE student SET email = 'test1@x.local' WHERE student_id = 1; (не COMMIT).
Сессия 2: SELECT email для student_id = 1 — какое значение? COMMIT в сессии 1; повторите SELECT.

### Задание 2. REPEATABLE READ

Сессия 1: BEGIN ISOLATION LEVEL REPEATABLE READ; SELECT COUNT(*) FROM student;
Сессия 2: INSERT нового студента; COMMIT;
Сессия 1: SELECT COUNT(*) снова — изменилось ли?

### Задание 3. Теория

Кратко опишите phantom read и как его предотвращает REPEATABLE READ в PostgreSQL.

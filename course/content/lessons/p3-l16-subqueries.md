## Подзапросы: scalar, IN, EXISTS

**Часть:** SQL: язык манипулирования и определения данных · **Модуль:** Агрегация и подзапросы

Практика выполняется в **PostgreSQL** (psql или pgAdmin). Сквозная предметная область — **университет** (студенты, группы, оценки).

### Цели урока

- Вложить SELECT во WHERE и FROM
- Использовать EXISTS для проверки наличия
- Сравнить подзапросы и JOIN

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 8, §8.1
2. **2-я очередь.** Линн Бейли — Изучаем SQL — Глава 13

Далее (по желанию):

- Уолтер Шилдс — SQL: быстрое погружение — Глава 8: подзапросы в SELECT и WHERE

### Краткая теория

**Подзапрос** (subquery) — SELECT, вложенный в другой SQL-оператор.

#### Скалярный подзапрос

Возвращает одно значение (одну строку, один столбец):

```sql
SELECT last_name, first_name
FROM student
WHERE student_id = (
    SELECT student_id FROM student WHERE email = 'ivanov@uni.local'
);

SELECT last_name, grade
FROM performance p
JOIN student s ON s.student_id = p.student_id
WHERE grade > (SELECT AVG(grade) FROM performance);
```

#### Подзапрос с IN

```sql
SELECT last_name FROM student
WHERE student_id IN (
    SELECT student_id FROM student_in_group WHERE group_id = 1
);
```

> **Осторожно с NOT IN и NULL:** если подзапрос возвращает NULL, результат может быть пустым. Предпочитайте `NOT EXISTS`.

#### EXISTS

Проверка наличия строк (коррелированный подзапрос):

```sql
SELECT name FROM subject subj
WHERE EXISTS (
    SELECT 1 FROM performance p
    WHERE p.subject_id = subj.subject_id
);
```

`EXISTS` останавливается на первом совпадении — часто эффективнее IN.

#### Подзапрос во FROM (производная таблица)

```sql
SELECT g.name, t.avg_grade
FROM s_group g
JOIN (
    SELECT sig.group_id, AVG(p.grade) AS avg_grade
    FROM student_in_group sig
    JOIN performance p ON p.student_id = sig.student_id
    GROUP BY sig.group_id
) t ON t.group_id = g.group_id;
```

#### Скалярный подзапрос в списке SELECT

Внутренний SELECT можно поставить и в список столбцов: одно значение (часто агрегат по всей таблице) повторяется рядом с каждой строкой внешнего запроса.

```sql
SELECT g.name,
       COUNT(sig.student_id) AS in_group,
       (SELECT COUNT(*) FROM student) AS all_students
FROM s_group g
LEFT JOIN student_in_group sig ON sig.group_id = g.group_id
GROUP BY g.name;
```

Позже тот же приём удобнее записать CTE. `DISTINCT` внутри подзапроса имеет смысл, когда нужен **список ключей без дублей** (например, `IN (SELECT DISTINCT student_id FROM performance)`). Для антисоединения всё равно предпочитайте `NOT EXISTS`, а не `NOT IN`.

#### Подзапрос vs JOIN

Многие запросы записываются обоими способами. JOIN обычно прозрачнее; EXISTS удобен для проверки существования.

Справочник: `course/sql/p3-l19-subqueries.sql`.

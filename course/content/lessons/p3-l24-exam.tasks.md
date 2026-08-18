## Итоговый контроль PostgreSQL

**Время:** 90 минут · **Схема:** `university` (полная загрузка из `p3-l22-lab-university.sql`)

### Часть A. DDL (20 баллов)

1. Создайте таблицу `scholarship(student_id, amount, from_date)` с FK на student и CHECK amount > 0.
2. Добавьте столбец `note TEXT` через ALTER TABLE.

### Часть B. DML (15 баллов)

3. INSERT стипендии 5000 для двух студентов с RETURNING.
4. UPDATE: увеличьте amount на 10% тем, у кого средний балл ≥ 4.5.
5. DELETE стипендий студентов без оценок (подзапрос).

### Часть C. SELECT (35 баллов)

6. INNER JOIN: фамилия, группа, дисциплина, оценка для курса 3.
7. LEFT JOIN: все группы и число студентов.
8. GROUP BY + HAVING: дисциплины со средним ≥ 4 и ≥ 2 оценок.
9. Подзапрос EXISTS: студенты с хотя бы одной «5».
10. UNION: фамилии студентов и преподавателей.

### Часть D. Транзакции и VIEW (20 баллов)

11. Транзакция: INSERT оценки + INSERT audit в одном COMMIT; ROLLBACK в втором прогоне.
12. CREATE VIEW `v_deans_report` — группа, средний балл, число студентов.

### Часть E. Теория (10 баллов)

13. WHERE vs HAVING; INNER vs LEFT JOIN; DELETE vs TRUNCATE — краткие определения.

**Сохраните решение:** `course/sql/p3-l24-exam-solution.sql`

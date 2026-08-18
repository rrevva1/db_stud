## Практика PostgreSQL

### Задание 1. VIEW

```sql
CREATE VIEW v_student_avg AS
SELECT s.student_id, s.last_name, AVG(p.grade)::numeric(4,2) AS avg_grade
FROM student s
LEFT JOIN performance p ON p.student_id = s.student_id
GROUP BY s.student_id, s.last_name;
```

### Задание 2. Использование

`SELECT * FROM v_student_avg WHERE avg_grade >= 4.5 ORDER BY avg_grade DESC;`

### Задание 3. MATERIALIZED VIEW

Создайте MV для статистики по группам. Измените данные, выполните REFRESH — сравните результат до и после.

**Справочник:** `course/sql/p3-l22-lab-university.sql`

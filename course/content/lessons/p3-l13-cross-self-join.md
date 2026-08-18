## CROSS JOIN и SELF JOIN

**Часть:** SQL: язык манипулирования и определения данных · **Модуль:** SELECT и соединения

Практика выполняется в **PostgreSQL** (psql или pgAdmin). Сквозная предметная область — **университет** (студенты, группы, оценки).

### Цели урока

- Построить декартово произведение
- Применить самосоединение для иерархий
- Оценить риски CROSS JOIN

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 6, §6.4
2. **2-я очередь.** Новиков Б. А. и др. — Основы технологий баз данных — Глава 5, §5.3
### Краткая теория

#### CROSS JOIN — декартово произведение

Каждая строка первой таблицы соединяется с **каждой** строкой второй:

```sql
SELECT s.last_name, g.name
FROM student s
CROSS JOIN s_group g;
```

Если в `student` 100 строк и в `s_group` 20 — результат 2000 строк.

**Риск:** случайный CROSS JOIN без условия в старом синтаксисе (`FROM a, b` без WHERE) создаёт огромный результат.

Полезные применения:
- Генерация комбинаций (расписание × аудитории).
- Явное декартово произведение с последующей фильтрацией.

#### SELF JOIN — самосоединение

Таблица соединяется **с самой собой** через алиасы:

```sql
-- пары студентов с одной фамилией
SELECT a.last_name, a.first_name AS first1, b.first_name AS first2
FROM student a
JOIN student b ON a.last_name = b.last_name AND a.student_id < b.student_id;
```

Условие `a.student_id < b.student_id` исключает дубликаты и пару (A,A).

#### Иерархии (руководитель — подчинённый)

```sql
CREATE TABLE employee (
    emp_id INT PRIMARY KEY,
    name VARCHAR(50),
    manager_id INT REFERENCES employee(emp_id)
);

SELECT e.name AS employee, m.name AS manager
FROM employee e
LEFT JOIN employee m ON e.manager_id = m.emp_id;
```

#### CROSS JOIN vs INNER JOIN

`INNER JOIN ... ON TRUE` эквивалентен `CROSS JOIN`.

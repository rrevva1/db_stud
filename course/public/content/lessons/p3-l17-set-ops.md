## Операции над множествами: UNION, INTERSECT, EXCEPT

**Часть:** SQL: язык манипулирования и определения данных · **Модуль:** Агрегация и подзапросы

Практика выполняется в **PostgreSQL** (psql или pgAdmin). Сквозная предметная область — **университет** (студенты, группы, оценки).

### Цели урока

- Объединить результаты запросов
- Убрать дубликаты UNION ALL
- Применить INTERSECT и EXCEPT

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 8, §8.2
2. **2-я очередь.** К. Дж. Дейт — SQL и реляционная теория — Глава 5
### Краткая теория

**Операции над множествами** объединяют результаты двух SELECT-запросов с **совместимыми** столбцами (число и типы).

#### UNION — объединение

```sql
SELECT last_name, first_name FROM student
UNION
SELECT last_name, first_name FROM student_archive;
```

`UNION` удаляет дубликаты. `UNION ALL` сохраняет все строки (быстрее):

```sql
SELECT email FROM student WHERE email IS NOT NULL
UNION ALL
SELECT email FROM teacher WHERE email IS NOT NULL;
```

#### INTERSECT — пересечение

```sql
SELECT student_id FROM student_in_group WHERE group_id = 1
INTERSECT
SELECT student_id FROM performance WHERE grade = 5;
-- студенты группы 1 с отличной оценкой
```

#### EXCEPT — разность

```sql
SELECT student_id FROM student
EXCEPT
SELECT student_id FROM performance;
-- студенты без оценок
```

#### Требования совместимости

- Одинаковое число столбцов.
- Совместимые типы (PostgreSQL приведёт к общему типу).
- Имена столбцов берутся из **первого** запроса.
- ORDER BY применяется к результату целиком:

```sql
(SELECT ... ) UNION (SELECT ... ) ORDER BY 1;
```

#### Связь с теорией

`UNION`, `INTERSECT`, `EXCEPT` — аналоги операций ∪, ∩, − реляционной алгебры.

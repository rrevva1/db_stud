## GROUP BY и агрегирование

**Часть:** SQL: язык манипулирования и определения данных · **Модуль:** Агрегация и подзапросы

Практика выполняется в **PostgreSQL** (psql или pgAdmin). Сквозная предметная область — **университет** (студенты, группы, оценки).

### Цели урока

- Группировать данные по столбцам
- Использовать COUNT, SUM, AVG, MIN, MAX
- Понять правило «все столбцы в GROUP BY»

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 7, §7.1
2. **2-я очередь.** Линн Бейли — Изучаем SQL — Глава 12

Далее (по желанию):

- Уолтер Шилдс — SQL: быстрое погружение — Глава 7: агрегаты и GROUP BY

### Краткая теория

**Агрегатные функции** сводят множество строк к одному значению:

| Функция | Назначение |
|---------|------------|
| `COUNT(*)` | Число строк |
| `COUNT(столбец)` | Число не-NULL значений |
| `SUM`, `AVG` | Сумма, среднее |
| `MIN`, `MAX` | Минимум, максимум |

#### GROUP BY

Группировка — «разбить строки на группы и агрегировать каждую»:

```sql
SELECT subj.name, AVG(p.grade)::numeric(4,2) AS avg_grade
FROM performance p
JOIN subject subj ON subj.subject_id = p.subject_id
GROUP BY subj.name;
```

#### Правило GROUP BY

В `SELECT` могут быть:
- столбцы из `GROUP BY`;
- агрегатные функции;
- выражения от них.

**Нельзя:** `SELECT last_name, AVG(grade) ... GROUP BY subject_id` — `last_name` не в GROUP BY (кроме функциональной зависимости в PostgreSQL при PK).

#### Несколько столбцов группировки

```sql
SELECT g.name, subj.name, AVG(p.grade)
FROM performance p
JOIN student_in_group sig ON sig.student_id = p.student_id
JOIN s_group g ON g.group_id = sig.group_id
JOIN subject subj ON subj.subject_id = p.subject_id
GROUP BY g.name, subj.name;
```

#### COUNT(*) vs COUNT(столбец)

```sql
SELECT COUNT(*) FROM student;           -- все строки
SELECT COUNT(email) FROM student;       -- без NULL email
```

Справочник: `course/sql/p3-l17-group-by.sql`.

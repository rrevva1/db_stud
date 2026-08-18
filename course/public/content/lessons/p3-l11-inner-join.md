## INNER JOIN: пересечение данных

**Часть:** SQL: язык манипулирования и определения данных · **Модуль:** SELECT и соединения

Практика выполняется в **PostgreSQL** (psql или pgAdmin). Сквозная предметная область — **университет** (студенты, группы, оценки).

### Цели урока

- Соединить две и более таблиц
- Использовать составные ключи
- Оптимизировать читаемость запроса

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 6, §6.2
2. **2-я очередь.** Братусь Н. В. и др. — Базы данных. Практикум — Задание 5: соединения

Далее (по желанию):

- Уолтер Шилдс — SQL: быстрое погружение — Глава 6: внутренние соединения

### Краткая теория

**INNER JOIN** возвращает только те строки, для которых условие соединения истинно в **обеих** таблицах.

#### Две таблицы

```sql
SELECT s.last_name, g.name AS group_name
FROM student s
INNER JOIN student_in_group sig ON sig.student_id = s.student_id
INNER JOIN s_group g ON g.group_id = sig.group_id;
```

#### Несколько таблиц

```sql
SELECT s.last_name, subj.name, p.grade
FROM performance p
JOIN student s ON s.student_id = p.student_id
JOIN subject subj ON subj.subject_id = p.subject_id
WHERE p.grade >= 4;
```

#### Составные ключи

Если связь по нескольким столбцам:

```sql
JOIN enrollment e
  ON e.student_id = s.student_id
 AND e.year = s.entry_year
```

#### Порядок JOIN и читаемость

Рекомендуется:
1. `FROM` — основная таблица (факт).
2. Последовательные `JOIN` — справочники.
3. `WHERE` — фильтрация после соединения.

#### Эквивалент через WHERE (устаревший стиль)

```sql
SELECT s.last_name, g.name
FROM student s, student_in_group sig, s_group g
WHERE sig.student_id = s.student_id
  AND g.group_id = sig.group_id;
```

Явный `JOIN` предпочтительнее: условие связи отделено от фильтрации.

#### План выполнения

СУБД может менять порядок соединений. На больших таблицах важны индексы на столбцах FK (Part 5).

Справочник: `course/sql/p3-l14-joins.sql`.

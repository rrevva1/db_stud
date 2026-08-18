## Скalarные функции и выражения

**Часть:** SQL: язык манипулирования и определения данных · **Модуль:** Функции, транзакции и объекты БД

Практика выполняется в **PostgreSQL** (psql или pgAdmin). Сквозная предметная область — **университет** (студенты, группы, оценки).

### Цели урока

- Использовать строковые и числовые функции
- Работать с датами и интервалами
- Применять COALESCE и NULLIF

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 9, §9.1
2. **2-я очередь.** Линн Бейли — Изучаем SQL — Глава 14

Далее (по желанию):

- Уолтер Шилдс — SQL: быстрое погружение — Глава 7: строковые и датовые функции (в курсе — PostgreSQL)

### Краткая теория

**Скalarные функции** возвращают одно значение для каждой строки (или для всего выражения).

#### Строковые функции

```sql
SELECT UPPER(last_name), LOWER(first_name),
       LENGTH(last_name), TRIM(email),
       SUBSTRING(last_name FROM 1 FOR 3),
       REPLACE(email, '@uni.local', '@alumni.local'),
       POSITION('@' IN email),
       CONCAT_WS(' ', last_name, first_name) AS fio
FROM student;
```

`CONCAT_WS` склеивает части через разделитель и пропускает NULL. `||` тоже конкатенация; `CONCAT` в PostgreSQL обрабатывает NULL как пустую строку. `REPLACE` / `POSITION` — замена и поиск подстроки (аналоги SQLite `REPLACE` / `INSTR`).

#### Числовые функции

```sql
SELECT ROUND(AVG(grade)::numeric, 2),
       CEIL(hours / 36.0),
       ABS(grade - 3),
       MOD(student_id, 2)
FROM performance;
```

#### Дата и время

```sql
SELECT NOW(), CURRENT_DATE,
       EXTRACT(YEAR FROM birth_date) AS y,
       AGE(birth_date) AS years_old,
       birth_date::date,   -- отбросить время, не SQLite DATE()
       birth_date + INTERVAL '1 year'
FROM student;
```

#### COALESCE и NULLIF

```sql
SELECT COALESCE(email, 'нет почты') FROM student;

SELECT NULLIF(grade, 0)   -- NULL если grade = 0, иначе grade
FROM performance;
```

`COALESCE(a, b, c)` — первый не-NULL аргумент.

#### Функции в WHERE и GROUP BY

```sql
WHERE EXTRACT(YEAR FROM birth_date) = 2004
GROUP BY DATE_TRUNC('month', grade_date)
```

## WHERE, ORDER BY и операторы сравнения

**Часть:** SQL: язык манипулирования и определения данных · **Модуль:** SELECT и соединения

Практика выполняется в **PostgreSQL** (psql или pgAdmin). Сквозная предметная область — **университет** (студенты, группы, оценки).

### Цели урока

- Фильтровать строки сложными условиями
- Сортировать по нескольким столбцам
- Применять BETWEEN, IN, LIKE

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 5, §5.2
2. **2-я очередь.** Братусь Н. В. и др. — Базы данных. Практикум — Глава 5: фильтрация

Далее (по желанию):

- Уолтер Шилдс — SQL: быстрое погружение — Глава 5: WHERE, LIKE, AND/OR

### Краткая теория

#### WHERE — фильтрация строк

```sql
SELECT last_name, first_name, birth_date
FROM student
WHERE birth_date >= '2004-01-01';
```

#### Логические операторы

```sql
WHERE course_num = 3 AND faculty_id = 1
WHERE last_name LIKE 'И%' OR last_name LIKE 'П%'
WHERE NOT email IS NULL
```

Приоритет: `NOT` → `AND` → `OR`. Используйте скобки для ясности.

#### Операторы сравнения

| Оператор | Пример |
|----------|--------|
| `=`, `<>`, `!=` | `grade <> 3` |
| `<`, `>`, `<=`, `>=` | `course_num >= 2` |
| `BETWEEN` | `birth_date BETWEEN '2003-01-01' AND '2004-12-31'` |
| `IN` | `group_id IN (1, 2, 5)` |
| `LIKE` | см. каталог ниже |
| `IS NULL` | `email IS NULL` |

> **Важно:** `WHERE email = NULL` всегда ложно! Используйте `IS NULL`.

#### Каталог LIKE

`%` — любая последовательность символов (в том числе пустая). `_` — ровно один символ.

| Шаблон | Смысл | Пример фамилии |
|--------|--------|----------------|
| `'И%'` | начинается с «И» | Иванов |
| `'%ов'` | заканчивается на «ов» | Петров |
| `'%ан%'` | содержит «ан» | Иванов, Антонов |
| `'И%в'` | начинается с «И» и заканчивается на «в» | Иванов |
| `'Иван_'` | «Иван» + ровно один символ | Ивана, не Иванов |
| `NOT LIKE 'И%'` | не начинается с «И» | Петров |

В PostgreSQL **`LIKE` чувствителен к регистру**: `'и%'` не найдёт `Иванов`. Для поиска без регистра используйте `ILIKE` (или `LOWER(last_name) LIKE 'и%'`). Чтобы искать сам символ `%` или `_`, задайте `ESCAPE`.

Скобки с `AND`/`OR` по **разным столбцам** — иначе приоритет `AND` над `OR` даст не ту выборку:

```sql
WHERE (last_name LIKE 'И%' OR last_name LIKE 'П%')
  AND birth_date >= '2004-01-01';
```

#### ORDER BY — сортировка

```sql
SELECT last_name, first_name, birth_date
FROM student
ORDER BY last_name ASC, first_name DESC;
```

Сортировка по выражению:

```sql
ORDER BY EXTRACT(YEAR FROM birth_date), last_name;
```

`NULL` по умолчанию идут последними при `ASC` (в PostgreSQL).

#### Комбинированный пример

```sql
SELECT s.last_name, g.name
FROM student s
JOIN student_in_group sig ON sig.student_id = s.student_id
JOIN s_group g ON g.group_id = sig.group_id
WHERE g.course_num IN (2, 3)
  AND s.last_name LIKE 'И%'
ORDER BY g.name, s.last_name
LIMIT 50;
```

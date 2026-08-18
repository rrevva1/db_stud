## DELETE и TRUNCATE

**Часть:** SQL: язык манипулирования и определения данных · **Модуль:** DML: изменение данных

Практика выполняется в **PostgreSQL** (psql или pgAdmin). Сквозная предметная область — **университет** (студенты, группы, оценки).

### Цели урока

- Удалить строки по условию
- Сравнить DELETE и TRUNCATE
- Учесть каскадное удаление

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 4, §4.3
2. **2-я очередь.** Линн Бейли — Изучаем SQL — Глава 8

Далее (по желанию):

- Уолтер Шилдс — SQL: быстрое погружение — Глава 10: удаление; сначала SELECT

### Краткая теория

Команды **DELETE** и **TRUNCATE** удаляют данные, но работают принципиально по-разному.

#### DELETE — построчное удаление

```sql
DELETE FROM student
WHERE student_id = 5;

DELETE FROM performance
WHERE grade_date < '2020-01-01';
```

Без `WHERE` удаляются **все** строки (таблица остаётся). Перед DELETE выполните `SELECT` с тем же условием.

#### DELETE … RETURNING

```sql
DELETE FROM student
WHERE email IS NULL
RETURNING student_id, last_name;
```

#### Каскадное удаление

При `ON DELETE CASCADE` на внешнем ключе удаление родителя автоматически удаляет дочерние строки:

```sql
-- student_in_group с ON DELETE CASCADE
DELETE FROM student WHERE student_id = 1;
-- удалятся и записи в student_in_group
```

#### TRUNCATE — быстрая очистка

```sql
TRUNCATE TABLE performance;
TRUNCATE TABLE student_in_group, student RESTART IDENTITY CASCADE;
```

| Свойство | DELETE | TRUNCATE |
|----------|--------|----------|
| Условие WHERE | Да | Нет (вся таблица) |
| Триггеры DELETE | Срабатывают | Не срабатывают |
| Откат в транзакции | Построчно | Да (DDL в транзакции PG) |
| Скорость на больших таблицах | Медленнее | Быстрее |

#### Выбор команды

- Удалить часть строк → `DELETE` с `WHERE`.
- Полностью очистить таблицу в тестах → `TRUNCATE`.
- Удалить таблицу и структуру → `DROP TABLE`.

## INSERT: добавление данных

**Часть:** SQL: язык манипулирования и определения данных · **Модуль:** DML: изменение данных

Практика выполняется в **PostgreSQL** (psql или pgAdmin). Сквозная предметная область — **университет** (студенты, группы, оценки).

### Цели урока

- Вставить одну и несколько строк
- Использовать INSERT … RETURNING
- Загрузить данные из SELECT

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 4, §4.1
2. **2-я очередь.** Линн Бейли — Изучаем SQL — Глава 7

Далее (по желанию):

- Уолтер Шилдс — SQL: быстрое погружение — Глава 10: DML vs анализ

### Краткая теория

**SELECT** задаёт вопросы к данным (анализ). **INSERT / UPDATE / DELETE** меняют общее хранилище (администрирование). Один синтаксис DML — разный риск: ошибка в SELECT ничего не портит, ошибка в INSERT видна всем.

Всегда указывайте **список столбцов** в INSERT: порядок и состав таблицы могут измениться.

**DML** (Data Manipulation Language) — команды для работы с данными. `INSERT` добавляет новые строки в таблицу.

#### Вставка одной строки

```sql
INSERT INTO student (last_name, first_name, birth_date)
VALUES ('Иванов', 'Пётр', '2003-05-12');
```

#### Вставка нескольких строк

```sql
INSERT INTO student (last_name, first_name, birth_date) VALUES
    ('Петрова', 'Анна', '2004-01-20'),
    ('Сидоров', 'Олег', '2003-11-03');
```

#### INSERT … RETURNING

PostgreSQL возвращает вставленные данные — удобно для получения сгенерированного `SERIAL`:

```sql
INSERT INTO student (last_name, first_name, birth_date)
VALUES ('Козлова', 'Мария', '2004-07-15')
RETURNING student_id, last_name;
```

#### INSERT … SELECT

Загрузка данных из другого запроса:

```sql
INSERT INTO student_archive (student_id, last_name, first_name)
SELECT student_id, last_name, first_name
FROM student
WHERE birth_date < '2000-01-01';
```

#### DEFAULT и NULL

```sql
INSERT INTO s_group (name, course_num) VALUES ('ИВТ-23', DEFAULT);
INSERT INTO student (last_name, first_name, birth_date, email)
VALUES ('Новиков', 'Иван', '2005-03-01', NULL);
```

#### Конфликты и UPSERT

```sql
INSERT INTO student (student_id, last_name, first_name, birth_date)
VALUES (1, 'Иванов', 'Пётр', '2003-05-12')
ON CONFLICT (student_id) DO UPDATE
    SET last_name = EXCLUDED.last_name;
```

Справочник: `course/sql/p3-l02-insert-select.sql`.

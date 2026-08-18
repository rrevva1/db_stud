## CREATE TABLE: создание таблиц и схем

**Часть:** SQL: язык манипулирования и определения данных · **Модуль:** DDL: определение структуры

Практика выполняется в **PostgreSQL** (psql или pgAdmin). Сквозная предметная область — **университет** (студенты, группы, оценки).

### Цели урока

- Создать таблицу с именованными столбцами
- Использовать схемы для организации объектов
- Применить IF NOT EXISTS и комментарии

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 3, §3.1
2. **2-я очередь.** Линн Бейли — Изучаем SQL — Глава 5
### Краткая теория

**DDL** (Data Definition Language) — подмножество SQL для описания структуры базы данных. Команда `CREATE TABLE` создаёт новое **отношение** (таблицу) с именованными **столбцами** (атрибутами) и их типами.

#### Синтаксис CREATE TABLE

```sql
CREATE TABLE [IF NOT EXISTS] имя_таблицы (
    столбец1 тип_данных [ограничения],
    столбец2 тип_данных [ограничения],
    ...
);
```

В PostgreSQL объекты организуются в **схемы** (`schema`). Схема `public` используется по умолчанию; для учебных проектов удобно создавать отдельную схему:

```sql
CREATE SCHEMA IF NOT EXISTS university;
SET search_path TO university, public;
```

#### Пример: таблицы студент и группа

```sql
CREATE TABLE student (
    student_id   SERIAL PRIMARY KEY,
    last_name    VARCHAR(50) NOT NULL,
    first_name   VARCHAR(50) NOT NULL,
    birth_date   DATE NOT NULL
);

CREATE TABLE s_group (
    group_id     SERIAL PRIMARY KEY,
    name         VARCHAR(20) NOT NULL UNIQUE,
    course_num   SMALLINT NOT NULL
);
```

`SERIAL` — псевдотип PostgreSQL: целое число с автоматически создаваемой последовательностью (аналог автоинкремента).

#### IF NOT EXISTS и комментарии

`CREATE TABLE IF NOT EXISTS` предотвращает ошибку при повторном запуске скрипта. Документирование:

```sql
COMMENT ON TABLE student IS 'Студенты университета';
COMMENT ON COLUMN student.birth_date IS 'Дата рождения';
```

#### Связующая таблица

Связь «студент — группа» многие-ко-многим реализуется таблицей `student_in_group`:

```sql
CREATE TABLE student_in_group (
    student_id   INT NOT NULL REFERENCES student(student_id),
    group_id     INT NOT NULL REFERENCES s_group(group_id),
    enrolled_at  DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (student_id, group_id)
);
```

#### Ключевые понятия

| Понятие | Описание |
|---------|----------|
| Отношение | Таблица в реляционной модели |
| Столбец (атрибут) | Именованное поле с фиксированным типом |
| Схема | Пространство имён для таблиц и других объектов |
| DDL | CREATE, ALTER, DROP — определение структуры |

> **Связь с теорией:** таблица SQL — физическая реализация отношения из реляционной модели (Part 1). Проектирование ER-модели (Part 2) предшествует написанию DDL.

Справочный скрипт: `course/sql/p3-l01-create-tables.sql`, базовая схема: `course/sql/schema-university.sql`.

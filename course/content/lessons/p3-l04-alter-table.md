## ALTER TABLE: изменение структуры

**Часть:** SQL: язык манипулирования и определения данных · **Модуль:** DDL: определение структуры

Практика выполняется в **PostgreSQL** (psql или pgAdmin). Сквозная предметная область — **университет** (студенты, группы, оценки).

### Цели урока

- Добавить и удалить столбцы
- Изменить тип данных и ограничения
- Переименовать таблицы и столбцы

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 3, §3.4
2. **2-я очередь.** Линн Бейли — Изучаем SQL — Глава 6
### Краткая теория

Команда **ALTER TABLE** изменяет структуру существующей таблицы без пересоздания данных (в большинстве случаев).

#### Добавление и удаление столбцов

```sql
ALTER TABLE student ADD COLUMN email VARCHAR(100);
ALTER TABLE student ADD COLUMN phone VARCHAR(20) DEFAULT NULL;

ALTER TABLE student DROP COLUMN phone;
ALTER TABLE student DROP COLUMN IF EXISTS temp_col;
```

Новый столбец без DEFAULT получает NULL во всех существующих строках.

#### Изменение типа и ограничений

```sql
ALTER TABLE student ALTER COLUMN email SET NOT NULL;
ALTER TABLE student ALTER COLUMN course_num TYPE INTEGER;

-- USING нужен при несовместимом преобразовании:
ALTER TABLE student ALTER COLUMN code TYPE VARCHAR(10) USING code::VARCHAR;
```

#### Добавление ограничений

```sql
ALTER TABLE student ADD CONSTRAINT uq_email UNIQUE (email);
ALTER TABLE student ADD CONSTRAINT fk_group
    FOREIGN KEY (group_id) REFERENCES s_group(group_id);
```

#### Переименование

```sql
ALTER TABLE student RENAME COLUMN fname TO first_name;
ALTER TABLE old_students RENAME TO student_archive;
```

#### Осторожность при изменениях

- Изменение типа на большой таблице может быть долгим (перезапись).
- Добавление `NOT NULL` требует, чтобы все строки уже имели значение.
- Удаление столбца необратимо без резервной копии.

> **Практикум:** после проектирования ER-модели (Part 2) схема эволюционирует через ALTER TABLE по мере уточнения требований.

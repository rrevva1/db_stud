## Ограничения: PRIMARY KEY, FOREIGN KEY, CHECK, UNIQUE

**Часть:** SQL: язык манипулирования и определения данных · **Модуль:** DDL: определение структуры

Практика выполняется в **PostgreSQL** (psql или pgAdmin). Сквозная предметная область — **университет** (студенты, группы, оценки).

### Цели урока

- Задать первичный и внешний ключи
- Добавить CHECK и UNIQUE ограничения
- Обработать ошибки нарушения целостности

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 3, §3.3
2. **2-я очередь.** Братусь Н. В. и др. — Базы данных. Практикум — Глава 4: ограничения
### Краткая теория

**Ограничения целостности** (constraints) — правила, которые СУБД проверяет при каждой операции INSERT/UPDATE. Они реализуют сущностную, ссылочную и доменную целостность.

#### PRIMARY KEY — первичный ключ

Уникально идентифицирует строку; не допускает NULL:

```sql
student_id SERIAL PRIMARY KEY
-- или составной:
PRIMARY KEY (student_id, group_id)
```

#### FOREIGN KEY — внешний ключ

Столбец (или набор столбцов) ссылается на PRIMARY KEY или UNIQUE другой таблицы:

```sql
group_id INT NOT NULL REFERENCES s_group(group_id)
    ON DELETE CASCADE
    ON UPDATE RESTRICT
```

| Действие | Поведение при удалении родителя |
|----------|-------------------------------|
| `RESTRICT` / `NO ACTION` | Запрет удаления |
| `CASCADE` | Каскадное удаление дочерних строк |
| `SET NULL` | Обнуление внешнего ключа |

#### UNIQUE, NOT NULL, CHECK

```sql
email VARCHAR(100) UNIQUE,
course_num SMALLINT NOT NULL CHECK (course_num BETWEEN 1 AND 6),
salary NUMERIC CHECK (salary > 0)
```

#### Именованные ограничения

```sql
CONSTRAINT chk_grade CHECK (grade BETWEEN 2 AND 5)
```

Имена упрощают диагностику ошибок:

```
ERROR: new row violates check constraint "chk_grade"
```

#### Обработка нарушений

При нарушении ограничения PostgreSQL откатывает операцию и возвращает ошибку. В приложении перехватывают SQLSTATE `23503` (FK), `23505` (UNIQUE), `23514` (CHECK).

Справочник: `course/sql/p3-l06-ddl-constraints.sql`.

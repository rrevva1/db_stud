## Транзакции: BEGIN, COMMIT, ROLLBACK

**Часть:** SQL: язык манипулирования и определения данных · **Модуль:** Функции, транзакции и объекты БД

Практика выполняется в **PostgreSQL** (psql или pgAdmin). Сквозная предметная область — **университет** (студенты, группы, оценки).

### Цели урока

- Оформить операции в транзакцию
- Откатить изменения при ошибке
- Понять свойства ACID

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 10, §10.1
2. **2-я очередь.** Новиков Б. А. и др. — Основы технологий баз данных — Глава 9, §9.2
### Краткая теория

**Транзакция** — логическая единица работы: набор операций выполняется **атомарно**.

#### Управление транзакциями

```sql
BEGIN;   -- или START TRANSACTION;

UPDATE account SET balance = balance - 1000 WHERE id = 1;
UPDATE account SET balance = balance + 1000 WHERE id = 2;

COMMIT;   -- зафиксировать
-- ROLLBACK;  -- откатить
```

В **psql** каждая команда без явного BEGIN выполняется в autocommit-режиме.

#### ACID

| Свойство | Смысл |
|----------|-------|
| **A**tomicity | Всё или ничего |
| **C**onsistency | БД остаётся в согласованном состоянии |
| **I**solation | Транзакции не меша друг другу (уровни изоляции) |
| **D**urability | Зафиксированные данные сохраняются после сбоя |

#### SAVEPOINT

```sql
BEGIN;
INSERT INTO student (last_name, first_name, birth_date)
VALUES ('Тест', 'Тест', '2000-01-01');
SAVEPOINT sp1;
DELETE FROM student WHERE last_name = 'Тест';
ROLLBACK TO sp1;   -- отменить DELETE, INSERT остаётся
COMMIT;
```

#### Ошибки и откат

При ошибке в транзакции PostgreSQL переводит её в состояние **aborted** — нужен `ROLLBACK` перед новыми командами.

#### Практический пример: перевод студента

```sql
BEGIN;
UPDATE student_in_group SET group_id = 2
WHERE student_id = 1 AND group_id = 1;
INSERT INTO audit_log (action, ts) VALUES ('transfer', NOW());
COMMIT;
```

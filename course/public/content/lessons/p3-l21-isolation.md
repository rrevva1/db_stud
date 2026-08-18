## Уровни изоляции и аномалии параллелизма

**Часть:** SQL: язык манипулирования и определения данных · **Модуль:** Функции, транзакции и объекты БД

Практика выполняется в **PostgreSQL** (psql или pgAdmin). Сквозная предметная область — **университет** (студенты, группы, оценки).

### Цели урока

- Настроить READ COMMITTED и REPEATABLE READ
- Распознать dirty read и phantom read
- Выбрать уровень изоляции для задачи

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 10, §10.2
2. **2-я очередь.** К. Дж. Дейт — Введение в системы баз данных (8-е изд.) — Глава 16
### Краткая теория

При **параллельном** выполнении транзакций без изоляции возможны **анomalies**.

#### Аномалии

| Аномалия | Описание |
|----------|----------|
| Dirty read | Чтение незафиксированных данных другой транзакции |
| Non-repeatable read | Повторное чтение — другое значение |
| Phantom read | Появление новых строк при повторном запросе |
| Serialization anomaly | Результат не эквивалентен никакому последовательному порядку |

#### Уровни изоляции в PostgreSQL

```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;   -- по умолчанию
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

| Уровень | Dirty read | Non-repeatable | Phantom |
|---------|------------|----------------|---------|
| READ UNCOMMITTED | — (PG как RC) | — | — |
| READ COMMITTED | Нет | Да | Да |
| REPEATABLE READ | Нет | Нет | Нет* |
| SERIALIZABLE | Нет | Нет | Нет |

*В PostgreSQL REPEATABLE READ использует snapshot и блокирует phantom для большинства случаев.

#### Пример REPEATABLE READ

```sql
-- Сессия 1
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT AVG(grade) FROM performance;  -- 4.2
-- Сессия 2: INSERT новой оценки; COMMIT;
SELECT AVG(grade) FROM performance;  -- всё ещё 4.2
COMMIT;
```

#### Выбор уровня

- OLTP по умолчанию: **READ COMMITTED**.
- Отчёты с согласованным снимком: **REPEATABLE READ**.
- Критичные финансовые операции: **SERIALIZABLE** (возможны откаты serialization failure).

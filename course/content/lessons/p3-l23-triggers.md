## Триггеры и хранимые функции PL/pgSQL

**Часть:** SQL: язык манипулирования и определения данных · **Модуль:** Функции, транзакции и объекты БД

Практика выполняется в **PostgreSQL** (psql или pgAdmin). Сквозная предметная область — **университет** (студенты, группы, оценки).

### Цели урока

- Создать BEFORE/AFTER триггер
- Написать простую функцию на PL/pgSQL
- Обеспечить аудит изменений

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 11, §11.2
2. **2-я очередь.** Новиков Б. А. и др. — Основы технологий баз данных — Глава 10, §10.3
### Краткая теория

**Триггер** — функция, автоматически вызываемая при INSERT/UPDATE/DELETE (или TRUNCATE).

#### Функция PL/pgSQL

```sql
CREATE OR REPLACE FUNCTION audit_student_change()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO student_audit (student_id, action, changed_at)
    VALUES (COALESCE(NEW.student_id, OLD.student_id), TG_OP, NOW());
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;
```

#### Создание триггера

```sql
CREATE TRIGGER trg_student_audit
AFTER INSERT OR UPDATE OR DELETE ON student
FOR EACH ROW EXECUTE FUNCTION audit_student_change();
```

| Параметр | Значения |
|----------|----------|
| Момент | `BEFORE`, `AFTER`, `INSTEAD OF` |
| Гранулярность | `FOR EACH ROW`, `FOR EACH STATEMENT` |
| Событие | `INSERT`, `UPDATE`, `DELETE` |

#### BEFORE vs AFTER

- **BEFORE** — может изменить NEW или отменить операцию (`RETURN NULL`).
- **AFTER** — логирование, каскадная логика (FK уже проверен).

#### NEW и OLD

- INSERT: только `NEW`.
- DELETE: только `OLD`.
- UPDATE: оба.

#### Практика аудита

Триггеры удобны для журналирования, но усложняют отладку и тестирование. Для сложной логики рассматривайте приложение или logical replication.

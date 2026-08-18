## Роли, привилегии GRANT и REVOKE

**Часть:** Администрирование и архитектуры нагрузок · **Модуль:** Безопасность и эксплуатация

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Создать роли и назначить права
- Ограничить доступ к схемам и таблицам
- Применить принцип наименьших привилегий

### Краткая теория

PostgreSQL: **ROLE** = пользователь или группа. `CREATE ROLE`, `GRANT`, `REVOKE`.

```sql
CREATE ROLE analyst NOLOGIN;
GRANT CONNECT ON DATABASE university TO analyst;
GRANT USAGE ON SCHEMA public TO analyst;
GRANT SELECT ON student, s_group TO analyst;
GRANT analyst TO user_ivan;  -- membership
REVOKE INSERT ON performance FROM analyst;
```

**Привилегии:** SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER, CREATE, USAGE.

**Схемы:** `GRANT USAGE ON SCHEMA` — вход в схему; затем права на объекты.

**Default privileges:** `ALTER DEFAULT PRIVILEGES` для будущих таблиц.

**Least privilege:** приложению — только нужные DML; DBA — отдельная роль; не использовать superuser в app.

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 21, §21.2
2. **2-я очередь.** Душан Петкович — Microsoft SQL Server 2012. Руководство для начинающих — Глава 9: безопасность
### Ключевые понятия

- **GRANT** — выдача прав.
- **REVOKE** — отзыв прав.
- **ROLE** — пользователь/группа.
- **Least privilege** — минимально необходимые права.

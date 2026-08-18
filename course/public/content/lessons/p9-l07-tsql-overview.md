## T-SQL: обзор для PostgreSQL-разработчика

**Часть:** Альтернативные СУБД и итоговая аттестация · **Модуль:** T-SQL, теория Дейта и итог

> **Сравнение диалектов:** T-SQL (SQL Server) ↔ PostgreSQL

Практика: сравнение синтаксиса; PostgreSQL — основная среда курса.

### Цели урока

- Сопоставить синтаксис T-SQL и PostgreSQL
- Использовать TOP и OFFSET/FETCH
- Применить переменные и batch

### Краткая теория

**T-SQL** — диалект Microsoft SQL Server. Курс использует PostgreSQL; этот урок — **сравнение диалектов**.

| Задача | T-SQL | PostgreSQL |
|--------|-------|------------|
| Top N | `SELECT TOP 10 * FROM t` | `SELECT * FROM t LIMIT 10` |
| Pagination | `OFFSET 10 ROWS FETCH NEXT 5 ROWS ONLY` | `LIMIT 5 OFFSET 10` |
| String concat | `'a' + 'b'` | `'a' \|\| 'b'` or concat() |
| Identity | `IDENTITY(1,1)` | `SERIAL` / `GENERATED ALWAYS AS IDENTITY` |
| Boolean | `BIT` | `BOOLEAN` |
| Date | `GETDATE()` | `now()` / `CURRENT_TIMESTAMP` |
| Batch | `GO` separator | Single transaction / `;` |

**Variables:**
```sql
-- T-SQL
DECLARE @x INT = 5;
-- PostgreSQL
DO $$ DECLARE x int := 5; BEGIN ... END $$;
```

**Schemas:** SQL Server dbo vs PostgreSQL public.

### Что читать в источниках

1. **1-я очередь.** Душан Петкович — Microsoft SQL Server 2012. Руководство для начинающих — Главы 1–4
2. **2-я очередь.** Ицик Бен-Ган и др. — Microsoft SQL Server 2012. Создание запросов — Главы 1–3
### Ключевые понятия

- **TOP** — T-SQL limit rows.
- **LIMIT** — PostgreSQL limit.
- **GO** — batch separator SSMS.
- **IDENTITY** — auto-increment T-SQL.

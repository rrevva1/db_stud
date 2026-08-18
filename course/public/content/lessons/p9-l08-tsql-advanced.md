## T-SQL: процедуры, функции и MERGE

**Часть:** Альтернативные СУБД и итоговая аттестация · **Модуль:** T-SQL, теория Дейта и итог

> **Сравнение диалектов:** T-SQL (SQL Server) ↔ PostgreSQL

Сравнение продвинутых конструкций T-SQL и PostgreSQL.

### Цели урока

- Написать stored procedure в T-SQL
- Использовать MERGE для upsert
- Применить error handling TRY/CATCH

### Краткая теория

**Stored procedures:**

```sql
-- T-SQL
CREATE PROC dbo.UpsertGrade @sid INT, @grade INT AS
BEGIN TRY
  MERGE performance AS t USING (SELECT @sid AS sid) s ON t.student_id = s.sid
  WHEN MATCHED THEN UPDATE SET grade = @grade
  WHEN NOT MATCHED THEN INSERT (student_id, grade) VALUES (@sid, @grade);
END TRY
BEGIN CATCH
  THROW;
END CATCH

-- PostgreSQL
CREATE OR REPLACE PROC upsert_grade(p_sid int, p_grade int)
LANGUAGE plpgsql AS $$
BEGIN
  INSERT INTO performance (student_id, grade) VALUES (p_sid, p_grade)
  ON CONFLICT (student_id) DO UPDATE SET grade = EXCLUDED.grade;
EXCEPTION WHEN OTHERS THEN RAISE;
END; $$;
```

| Feature | T-SQL | PostgreSQL |
|---------|-------|------------|
| MERGE | Native MERGE (2019+) | INSERT ON CONFLICT |
| Error handling | TRY/CATCH | EXCEPTION block |
| Procedures | CREATE PROC | CREATE PROCEDURE (PG14+) |
| Table variables | @t TABLE | TEMP TABLE |
| Output inserted | OUTPUT clause | RETURNING |

### Что читать в источниках

1. **1-я очередь.** Ицик Бен-Ган и др. — Microsoft SQL Server 2012. Создание запросов — Главы 10–11
2. **2-я очередь.** Elizabeth Noble — Pro T-SQL 2019 — Главы 5–7
### Ключевые понятия

- **MERGE** — upsert T-SQL.
- **ON CONFLICT** — upsert PostgreSQL.
- **TRY/CATCH** — T-SQL errors.
- **RETURNING** — PG output clause.

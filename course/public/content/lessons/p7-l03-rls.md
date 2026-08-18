## Row-Level Security (RLS)

**Часть:** Администрирование и архитектуры нагрузок · **Модуль:** Безопасность и эксплуатация

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Включить RLS на таблице
- Написать политику USING/WITH CHECK
- Протестировать изоляцию строк

### Краткая теория

**RLS** — фильтрация строк по политикам на уровне СУБД (не только в приложении).

```sql
ALTER TABLE performance ENABLE ROW LEVEL SECURITY;
CREATE POLICY perf_student ON performance
  FOR SELECT TO student_role
  USING (student_id = current_setting('app.student_id')::int);
CREATE POLICY perf_ins ON performance FOR INSERT TO student_role
  WITH CHECK (student_id = current_setting('app.student_id')::int);
```

**USING** — какие строки видны; **WITH CHECK** — какие можно вставить/обновить.

**BYPASSRLS** — атрибут роли (админ); **SECURITY DEFINER** функции — осторожно.

Сравнение с SQL Server: там тоже RLS (security predicates); в PostgreSQL — policies на таблице.

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 21, §21.3
2. **2-я очередь.** Elizabeth Noble — Pro T-SQL 2019 — Глава 15: RLS в SQL Server
### Ключевые понятия

- **RLS** — безопасность на уровне строк.
- **USING** — фильтр чтения.
- **WITH CHECK** — ограничение записи.
- **Policy** — именованное правило.

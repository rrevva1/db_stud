## Практика PostgreSQL

### Задание 1. Таблица аудита

```sql
CREATE TABLE student_audit (
    audit_id SERIAL PRIMARY KEY,
    student_id INT,
    action TEXT,
    changed_at TIMESTAMP DEFAULT NOW()
);
```

### Задание 2. Функция и триггер

AFTER INSERT OR UPDATE OR DELETE на `student` — запись в `student_audit` с `TG_OP`.

### Задание 3. Тест

INSERT, UPDATE, DELETE одного студента. Проверьте 3 строки в audit.

### Вопрос

Чем BEFORE отличается от AFTER для аудита?

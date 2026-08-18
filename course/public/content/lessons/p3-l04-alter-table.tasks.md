## Практика PostgreSQL

### Задание 1. Новый столбец

```sql
ALTER TABLE university.student ADD COLUMN phone VARCHAR(20);
UPDATE university.student SET phone = '+7-900-000-00-01' WHERE student_id = 1;
```

### Задание 2. NOT NULL

Заполните `phone` для всех студентов, затем `ALTER COLUMN phone SET NOT NULL`.

### Задание 3. Переименование

Переименуйте столбец `phone` в `phone_number`. Переименуйте таблицу `type_lab` → `type_lab_archive` (если создавали на прошлом уроке).

### Задание 4. DROP

Удалите столбец `phone_number` командой `DROP COLUMN IF EXISTS`.

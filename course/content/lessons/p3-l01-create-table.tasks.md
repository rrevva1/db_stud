## Практика PostgreSQL

**Подготовка:** выполните `\\i course/sql/schema-university.sql` или создайте схему `lab` самостоятельно.

### Задание 1. Схема и таблицы

Создайте схему `lab` и таблицы `student`, `s_group`, `student_in_group` по образцу из `course/sql/p3-l01-create-tables.sql`. Добавьте комментарии к таблицам.

### Задание 2. IF NOT EXISTS

Напишите скрипт, который можно запускать повторно без ошибок (используйте `IF NOT EXISTS`).

### Задание 3. Проверка

Выполните `\\d lab.student` и `\\d lab.s_group` в psql. Убедитесь, что первичные ключи созданы.

### Самопроверка

- [ ] Три таблицы созданы в схеме `lab`
- [ ] `student_in_group` имеет составной PRIMARY KEY
- [ ] Скрипт идемпотентен

**Решение сохраните в:** `course/sql/p3-l01-create-table-solution.sql`

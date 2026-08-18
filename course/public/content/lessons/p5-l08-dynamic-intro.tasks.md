## Практика PostgreSQL

### Задание 1. EXECUTE с USING

Функция `get_student_by_id(p_id int)` — динамический SELECT с `$1` и USING.

### Задание 2. format и %I

Функция `count_in_table(p_schema text, p_table text)` — только `format` + `%I`. Попробуйте передать `'; DROP TABLE--'` — должна быть ошибка, не инъекция.

### Задание 3. regclass

Функция принимает `regclass`, считает строки через `format('SELECT count(*) FROM %s', tab)`.

### Задание 4. Отчёт с одним фильтром

Динамически добавляйте `AND column = $n` только для не-NULL параметров (безопасно).

### Самопроверка

- [ ] Значения — через USING или %L
- [ ] Идентификаторы — через %I или regclass
- [ ] Нет конкатенации сырого user input

Сохраните: `course/sql/p5-l08-dynamic-intro-solution.sql`

## Практика PostgreSQL

### Задание 1. Pivot через FILTER

Таблица `sales(department, quarter, amount)`. Постройте сводку: строки — отделы, столбцы — Q1–Q4, значения — сумма продаж.

### Задание 2. Pivot оценок

По `(student_id, semester, grade)` выведите матрицу: студент × семестр (1–8). Пропуски — NULL.

### Задание 3. crosstab

Установите `tablefunc` и повторите задание 1 через `crosstab`. Сравните читаемость с FILTER.

### Задание 4. Unpivot

Имея широкую таблицу из задания 1, верните длинный формат `(department, quarter, amount)` через `UNION ALL` или `CROSS JOIN LATERAL VALUES`.

### Самопроверка

- [ ] Суммы по строкам pivot сходятся с исходными данными
- [ ] NULL в ячейке означает отсутствие продаж, а не ноль (осознанный выбор)
- [ ] crosstab: категории в том же порядке, что в AS ct(...)

Сохраните: `course/sql/p4-l04-pivot-solution.sql`

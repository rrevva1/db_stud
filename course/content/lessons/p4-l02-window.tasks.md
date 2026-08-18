## Практика PostgreSQL

### Задание 1. Топ-3 по группам

Для таблицы `performance(student_id, subject, grade)` выведите топ-3 оценки **в каждой** группе студентов (через JOIN с `student` → `s_group`). Используйте `ROW_NUMBER() OVER (PARTITION BY group_id ORDER BY grade DESC)`.

### Задание 2. Сравнение с предыдущим периодом

Таблица продаж `(sale_date, amount)`. Вычислите разницу `amount - LAG(amount)` и процент изменения относительно предыдущего дня.

### Задание 3. Скользящее среднее

Постройте 7-дневное скользящее среднее выручки:

```sql
AVG(amount) OVER (
    ORDER BY sale_date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
)
```

### Задание 4. Накопительная сумма

По каждому `department_id` выведите накопительную сумму зарплат в порядке убывания `salary`.

### Задание 5. NTILE

Разбейте студентов на 4 квартиля по среднему баллу (`NTILE(4) OVER (ORDER BY avg_grade)`).

### Самопроверка

- [ ] PARTITION BY задаёт «независимые» окна
- [ ] ORDER BY в OVER обязателен для LAG/LEAD и накопительных сумм
- [ ] Результат содержит столько же строк, сколько исходный набор (без GROUP BY)

Сохраните: `course/sql/p4-l02-window-solution.sql`

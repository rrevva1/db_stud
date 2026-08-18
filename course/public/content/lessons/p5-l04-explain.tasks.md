## Практика PostgreSQL

См. демо: `course/sql/p5-l03-explain-analyze.sql`

### Задание 1. Базовый EXPLAIN

Выполните EXPLAIN и EXPLAIN ANALYZE для простого SELECT по PK и по неиндексированному столбцу. Сравните узлы.

### Задание 2. JOIN

Запрос с JOIN двух таблиц (100k+ строк). Определите: Nested Loop, Hash Join или Merge Join? Почему?

### Задание 3. Оценка vs факт

Намеренно создайте условие с неверной статистикой (много NULL без ANALYZE). Запустите ANALYZE и сравните plans.

### Задание 4. BUFFERS

EXPLAIN (ANALYZE, BUFFERS) для тяжёлого запроса. Посчитайте долю shared hit vs read.

### Задание 5. Индекс

Один и тот же запрос до/после CREATE INDEX — зафиксируйте смену Seq Scan → Index Scan.

### Самопроверка

- [ ] Читаете actual time и rows
- [ ] Понимаете cost — относительная мера
- [ ] Не используете enable_seqscan=off в production без причины

Сохраните: `course/sql/p5-l04-explain-solution.sql`

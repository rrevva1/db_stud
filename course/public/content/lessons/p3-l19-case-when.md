## Условные выражения CASE и CAST

**Часть:** SQL: язык манипулирования и определения данных · **Модуль:** Функции, транзакции и объекты БД

Практика выполняется в **PostgreSQL** (psql или pgAdmin). Сквозная предметная область — **университет** (студенты, группы, оценки).

### Цели урока

- Построить ветвление CASE WHEN
- Приводить типы CAST и ::
- Создать вычисляемые столбцы

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 9, §9.2
2. **2-я очередь.** Братусь Н. В. и др. — Базы данных. Практикум — Глава 6: выражения

Далее (по желанию):

- Уолтер Шилдс — SQL: быстрое погружение — Глава 5: CASE как классификатор

### Краткая теория

#### CASE — условное выражение

```sql
SELECT last_name, grade,
    CASE
        WHEN grade = 5 THEN 'отлично'
        WHEN grade = 4 THEN 'хорошо'
        WHEN grade = 3 THEN 'удовлетворительно'
        ELSE 'неуд'
    END AS rating_text
FROM performance p
JOIN student s ON s.student_id = p.student_id;
```

Простая форма (по значению):

```sql
CASE grade WHEN 5 THEN 'A' WHEN 4 THEN 'B' ELSE 'C' END
```

#### CAST и оператор ::

Приведение типов:

```sql
SELECT AVG(grade)::numeric(4,2);
SELECT CAST(birth_date AS TIMESTAMP);
SELECT '2024-01-15'::DATE;
```

#### Вычисляемые столбцы

```sql
SELECT last_name,
       EXTRACT(YEAR FROM AGE(birth_date)) AS age,
       CASE WHEN email IS NULL THEN FALSE ELSE TRUE END AS has_email
FROM student;
```

#### CASE в агрегатах

```sql
SELECT COUNT(CASE WHEN grade = 5 THEN 1 END) AS fives,
       COUNT(CASE WHEN grade < 4 THEN 1 END) AS poor
FROM performance;
```

Аналог `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`.

CASE удобен как **классификатор**: новый столбец-метка (курс/риск/категория), а не только перевод оценки в слово. Всегда продумывайте `ELSE`: иначе «хвост» станет тихим `NULL`.

В PostgreSQL **алиас столбца CASE нельзя использовать в WHERE** того же запроса (алиасы появляются на шаге SELECT, позже WHERE). Повторите выражение, оберните в подзапрос или CTE:

```sql
SELECT *
FROM (
    SELECT last_name,
           CASE WHEN birth_date >= '2004-01-01' THEN 'младше'
                ELSE 'старше' END AS age_band
    FROM student
) t
WHERE age_band = 'младше';
```

#### CASE vs COALESCE

`COALESCE` — частный случай для NULL; `CASE` — произвольная логика.

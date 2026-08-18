## LEFT, RIGHT и FULL OUTER JOIN

**Часть:** SQL: язык манипулирования и определения данных · **Модуль:** SELECT и соединения

Практика выполняется в **PostgreSQL** (psql или pgAdmin). Сквозная предметная область — **университет** (студенты, группы, оценки).

### Цели урока

- Сохранить строки без пары
- Обработать NULL при внешнем соединении
- Выбрать подходящий тип OUTER JOIN

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 6, §6.3
2. **2-я очередь.** Линн Бейли — Изучаем SQL — Глава 11

Далее (по желанию):

- Уолтер Шилдс — SQL: быстрое погружение — Глава 6: LEFT JOIN и несовпавшие строки

### Краткая теория

**Внешние соединения** (OUTER JOIN) сохраняют строки «без пары» из одной или обеих таблиц.

#### LEFT OUTER JOIN

Все строки из **левой** таблицы + совпадения справа:

```sql
SELECT g.name, s.last_name
FROM s_group g
LEFT JOIN student_in_group sig ON sig.group_id = g.group_id
LEFT JOIN student s ON s.student_id = sig.student_id
ORDER BY g.name, s.last_name;
```

Группы без студентов: `s.last_name IS NULL`.

#### RIGHT OUTER JOIN

Зеркально LEFT — все строки справа:

```sql
SELECT s.last_name, g.name
FROM student_in_group sig
RIGHT JOIN s_group g ON g.group_id = sig.group_id
RIGHT JOIN student s ON s.student_id = sig.student_id;
```

PostgreSQL **поддерживает** RIGHT и FULL. Переписать RIGHT как LEFT — привычка переносимости и читаемости, а не требование СУБД: поменяйте таблицы местами.

```sql
-- тот же набор, что RIGHT JOIN s_group, но читается слева направо
SELECT s.last_name, g.name
FROM s_group g
LEFT JOIN student_in_group sig ON sig.group_id = g.group_id
LEFT JOIN student s ON s.student_id = sig.student_id;
```

Приём **несовпавших строк** (аудит «сирот»): LEFT JOIN и фильтр `IS NULL` по ключу правой стороны — группы без студентов, студенты без оценок и т. п.

#### FULL OUTER JOIN

Объединяет LEFT и RIGHT — строки без пары с обеих сторон:

```sql
SELECT s.last_name, g.name
FROM student s
FULL OUTER JOIN student_in_group sig ON sig.student_id = s.student_id
FULL OUTER JOIN s_group g ON g.group_id = sig.group_id;
```

#### Обработка NULL

При OUTER JOIN отсутствующие столбцы — `NULL`. Фильтрация:

```sql
WHERE s.student_id IS NULL   -- только «сироты» справа
```

**Ловушка:** `WHERE s.last_name = 'Иванов'` отфильтрует NULL-строки! Для сохранения используйте условие в `ON`:

```sql
LEFT JOIN student s ON s.student_id = sig.student_id AND s.last_name = 'Иванов'
```

#### Когда использовать

- Отчёт «все группы и число студентов» → LEFT JOIN + COUNT.
- Сравнение двух списков → FULL OUTER JOIN.

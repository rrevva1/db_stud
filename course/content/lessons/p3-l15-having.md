## HAVING: фильтрация групп

**Часть:** SQL: язык манипулирования и определения данных · **Модуль:** Агрегация и подзапросы

Практика выполняется в **PostgreSQL** (psql или pgAdmin). Сквозная предметная область — **университет** (студенты, группы, оценки).

### Цели урока

- Отличить WHERE от HAVING
- Фильтровать агрегированные результаты
- Комбинировать GROUP BY и HAVING

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 7, §7.2
2. **2-я очередь.** Братусь Н. В. и др. — Базы данных. Практикум — Задание 6: агрегаты

Далее (по желанию):

- Уолтер Шилдс — SQL: быстрое погружение — Глава 7: WHERE vs HAVING

### Краткая теория

#### WHERE vs HAVING

| | WHERE | HAVING |
|---|-------|--------|
| Применяется к | Отдельным строкам | Группам |
| Момент фильтрации | До группировки | После GROUP BY |
| Агрегаты | Нельзя (обычно) | Можно |

Двухступенчатый фильтр: **WHERE** отбрасывает **строки** до группировки; **HAVING** отбрасывает уже посчитанные **группы**. В PostgreSQL `HAVING` без `GROUP BY` допустим: вся таблица считается одной группой — не делайте из этого правило «HAVING запрещён без GROUP BY».

```sql
SELECT g.name, AVG(p.grade) AS avg_grade
FROM s_group g
JOIN student_in_group sig ON sig.group_id = g.group_id
JOIN performance p ON p.student_id = sig.student_id
WHERE g.course_num = 3              -- фильтр строк до группировки
GROUP BY g.name
HAVING AVG(p.grade) >= 4.0;         -- фильтр групп
```

#### Типичные задачи HAVING

```sql
-- группы с более чем 5 студентами
SELECT g.name, COUNT(sig.student_id) AS cnt
FROM s_group g
JOIN student_in_group sig ON sig.group_id = g.group_id
GROUP BY g.name
HAVING COUNT(sig.student_id) > 5;

-- дисциплины с разбросом оценок
SELECT subj.name, MAX(p.grade) - MIN(p.grade) AS spread
FROM performance p
JOIN subject subj ON subj.subject_id = p.subject_id
GROUP BY subj.name
HAVING MAX(p.grade) - MIN(p.grade) > 2;
```

#### Порядок выполнения

FROM → WHERE → GROUP BY → **HAVING** → SELECT → ORDER BY

#### Частая ошибка

Фильтр по агрегату в WHERE — синтаксическая ошибка:

```sql
-- НЕВЕРНО:
WHERE AVG(grade) > 4

-- ВЕРНО:
HAVING AVG(grade) > 4
```

## OLAP-кубы и операции drill-down

**Часть:** Хранилища данных · **Модуль:** DWH и dimensional modeling

Фокус на теории и тесте; SQL не обязателен.

### Цели урока

- Выполнить slice, dice, roll-up
- Объяснить ROLAP vs MOLAP
- Построить простой OLAP-отчёт

### Краткая теория

**OLAP operations:**
- **Slice** — фиксируем одно измерение (semester=1).
- **Dice** — подcube по нескольким фильтрам.
- **Roll-up** — агрегация вверх (день → месяц → год).
- **Drill-down** — детализация (faculty → group → student).

**ROLAP:** SQL over star schema (PostgreSQL, ClickHouse).
**MOLAP:** precomputed cube (SSAS, Essbase) — быстрый, less flexible.
**HOLAP:** hybrid.

SQL roll-up:
```sql
SELECT d.year, d.semester, avg(f.grade)
FROM fact_grade f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY ROLLUP (d.year, d.semester);
```

Smirnov: куб = метрика по осям dimensions; pivot tables в Excel — простой OLAP UI.

### Что читать в источниках

1. **1-я очередь.** Новиков Б. А. и др. — Основы технологий баз данных — Глава 17, §17.2
2. **2-я очередь.** Смирнов М. В. — Проектирование хранилищ данных — Глава 6
### Ключевые понятия

- **Slice/Dice** — выбор подмножества куба.
- **Roll-up** — агрегация.
- **ROLAP** — SQL-based OLAP.
- **MOLAP** — multidimensional storage.

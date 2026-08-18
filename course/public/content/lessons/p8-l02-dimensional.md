## Измерения и факты: основы dimensional modeling

**Часть:** Хранилища данных · **Модуль:** DWH и dimensional modeling

Фокус на теории и тесте; SQL не обязателен.

### Цели урока

- Выделить fact и dimension таблицы
- Определить grain фактовой таблицы
- Спроектировать surrogate key

### Краткая теория

**Fact table** — метрики (measures): оценка, сумма продаж, количество. **Grain** — что означает одна строка («одна оценка студента за экзамен»).

**Dimension** — контекст: студент, время, дисциплина, группа. Denormalized атрибуты для удобства фильтрации.

**Surrogate key** — искусственный PK dimension (student_key), отдельно от business key (student_id из OLTP).

**Types of facts:** additive (sum), semi-additive (balance), non-additive (ratio).

Пример университета:
- Fact: `fact_performance` (student_key, date_key, subject_key, grade)
- Dim: `dim_student`, `dim_date`, `dim_subject`

**Slowly Changing Dimensions (SCD):** Type 1 overwrite; Type 2 history rows with effective dates.

### Что читать в источниках

1. **1-я очередь.** Смирнов М. В. — Проектирование хранилищ данных — Глава 3
2. **2-я очередь.** конспект — Информационное обеспечение — Раздел 5: измерения
### Ключевые понятия

- **Fact** — таблица метрик.
- **Dimension** — контекст анализа.
- **Grain** — детализация строки факта.
- **Surrogate key** — суррогатный ключ.

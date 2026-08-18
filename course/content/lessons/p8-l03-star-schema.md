## Звезда (Star Schema)

**Часть:** Хранилища данных · **Модуль:** DWH и dimensional modeling

Фокус на теории и тесте; SQL не обязателен.

### Цели урока

- Построить star schema для продаж
- Денormalize измерения
- Оценить производительность запросов

### Краткая теория

**Star schema:** центральная **fact** + **dimensions** вокруг (радиальная схема). Dimensions **denormalized** (все атрибуты группы в dim_student).

```
        dim_date
            |
dim_student — fact_performance — dim_subject
            |
        dim_group
```

**Плюсы:** простые JOIN, быстрые агрегаты для BI, понятно бизнесу.
**Минусы:** redundancy в dimensions, риск inconsistency без ETL discipline.

**Запрос:** средний балл по факультетам за семестр — JOIN fact + dim_student + dim_date, GROUP BY faculty.

**Университет (design task):** grain = одна оценка; facts: grade, attempt; dims: student (name, group_id, faculty), date (semester, year), subject (name, department).

### Что читать в источниках

1. **1-я очередь.** Братусь Н. В. и др. — Базы данных. Практикум — Глава 8: star schema
2. **2-я очередь.** Смирнов М. В. — Проектирование хранилищ данных — Глава 4, §4.1
### Ключевые понятия

- **Star schema** — fact + denormalized dims.
- **Fact table** — центр звезды.
- **Denormalization** — для скорости чтения.

Сквозная предметная область: **университет** — звезда для успеваемости.

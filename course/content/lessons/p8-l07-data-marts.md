## Витрины данных (Data Marts)

**Часть:** Хранилища данных · **Модуль:** DWH и dimensional modeling

Фокус на теории и тесте; SQL не обязателен.

### Цели урока

- Спроектировать subject-area mart
- Определить SLA обновления
- Интегрировать mart с DWH

### Краткая теория

**Data Mart** — subset DWH для одной предметной области (деанат, admissions, finance).

**Dependent mart** — из enterprise DWH (Inmon).
**Independent mart** — Kimball standalone star для быстрого старта.

**SLA:** nightly batch vs hourly incremental; freshness vs cost.

**University marts:**
- **Mart успеваемости** — fact_grade + dims; users: деканат.
- **Mart контингента** — dim_student snapshots; users: учебный отдел.

**Integration:** conformed dimensions (dim_date, dim_student) across marts для cross-reporting.

**Security:** mart-level GRANT; row filters по faculty (аналог RLS в presentation layer).

### Что читать в источниках

1. **1-я очередь.** Смирнов М. В. — Проектирование хранилищ данных — Глава 7
2. **2-я очередь.** конспект — Информационное обеспечение — Раздел 6: витрины
### Ключевые понятия

- **Data Mart** — предметная витрина.
- **SLA** — соглашение о свежести.
- **Conformed dimension** — сквозное измерение.

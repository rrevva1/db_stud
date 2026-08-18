## OLTP vs OLAP: сравнение нагрузок

**Часть:** Администрирование и архитектуры нагрузок · **Модуль:** Безопасность и эксплуатация

Фокус на теории и тесте; SQL не обязателен.

### Цели урока

- Различить транзакционную и аналитическую нагрузку
- Сопоставить нормализацию и денormalization
- Выбрать архитектуру под сценарий

### Краткая теория

**OLTP:** много коротких транзакций (INSERT оценки, UPDATE профиля). 3NF, индексы на PK/FK, row-level locks, low latency.

**OLAP:** тяжёлые read, агрегаты, scan больших объёмов. Star schema, denormalized dimensions, columnar (ClickHouse, etc.), batch load.

| | OLTP | OLAP |
|---|------|------|
| Запросы | Короткие точечные | Scan + GROUP BY |
| Схема | Нормализованная | Star/snowflake |
| Consistency | Strong ACID | Often eventual in loads |
| Пример | university OLTP | DWH успеваемости |

**CAP (Brewer):** в partition — выбор **C** (consistency) vs **A** (availability). PostgreSQL sync rep → CP; async → AP bias с lag.

**HTAP:** гибриды (PostgreSQL + columnar extension) — компромисс.

Архитектура: OLTP → ETL/CDC → DWH для отчётов; не гонять OLAP на primary без replica.

### Что читать в источниках

1. **1-я очередь.** Дзгоев А. Э. — Проектирование и разработка баз и хранилищ данных. Лекция 1 — Слайды 80–95
2. **2-я очередь.** Смирнов М. В. — Проектирование хранилищ данных — Глава 1: OLTP и OLAP
### Ключевые понятия

- **OLTP** — транзакционная нагрузка.
- **OLAP** — аналитическая нагрузка.
- **CAP** — consistency/availability/partition.
- **Denormalization** — для аналитики.

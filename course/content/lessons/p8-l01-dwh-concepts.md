## Хранилища данных: понятия и архитектура

**Часть:** Хранилища данных · **Модуль:** DWH и dimensional modeling

Фокус на теории и тесте; SQL не обязателен.

### Цели урока

- Определить DWH, Data Mart и Data Lake
- Описать слои staging и core
- Сопоставить Inmon и Kimball

### Краткая теория

**DWH (Data Warehouse)** — предметно-ориентированное, интегрированное, неvolatile, time-variant хранилище для аналитики (Inmon).

**Data Mart** — витрина под департамент (продажи, успеваемость).

**Data Lake** — сырьё (raw files) в object storage; schema-on-read.

**Слои:**
- **Staging** — сырые копии из источников (OLTP).
- **Core/Integration** — очистка, conform dimensions (Inmon bus architecture).
- **Presentation** — star schemas, marts, reports.

**Inmon:** сверху-вниз, normalized enterprise DWH → marts.
**Kimball:** снизу-вверх, dimensional star schemas по процессам (факты + измерения).

Для **университета:** источник — OLTP (student, performance); DWH — история успеваемости, агрегаты по группам/кафедрам.

### Что читать в источниках

1. **1-я очередь.** Дзгоев А. Э. — Проектирование и разработка баз и хранилищ данных. Лекция 1 — Слайды 96–110
2. **2-я очередь.** Смирнов М. В. — Проектирование хранилищ данных — Глава 1–2
### Ключевые понятия

- **DWH** — аналитическое хранилище.
- **Staging** — промежуточная зона.
- **Inmon** — корпоративное DWH.
- **Kimball** — dimensional modeling.

## Контроль: проектирование хранилищ данных

**Часть:** Хранилища данных · **Модуль:** DWH и dimensional modeling

Итоговый тест части.

### Цели урока

- Спроектировать dimensional model
- Обосновать выбор star/snowflake
- Описать pipeline загрузки данных

### Краткая теория

Итог части 8: Inmon/Kimball, facts/dimensions/grain, star/snowflake, ETL/ELT, OLAP ops, marts.

**Экзаменационный кейс:** университет — построить DWH успеваемости: star schema, ETL из OLTP, OLAP запрос (roll-up по faculty), SLA mart для деканата.

### Что читать в источниках

1. **1-я очередь.** Дзгоев А. Э. — Проектирование и разработка баз и хранилищ данных. Лекция 1 — Слайды 96–120 (повторение)
2. **2-я очередь.** Смирнов М. В. — Проектирование хранилищ данных — Главы 1–8 (повторение)
### Ключевые понятия

- **Dimensional model** — facts+dims.
- **Star** — denormalized.
- **ETL** — pipeline.
- **OLAP** — slice/roll-up.

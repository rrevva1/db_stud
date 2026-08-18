## К. Дж. Дейт: продвинутая реляционная теория

**Часть:** Альтернативные СУБД и итоговая аттестация · **Модуль:** T-SQL, теория Дейта и итог

Фокус на теории и тесте; SQL не обязателен.

### Цели урока

- Обсудить NULL и реляционную модель
- Разобрать view updating problem
- Оценить соответствие SQL теории

### Краткая теория

**К. Дж. Дейт** критически оценивает SQL с позиции реляционной теории.

**NULL:** SQL ternary logic (TRUE/FALSE/UNKNOWN); Date: NULL нарушает информационную целостность — «missing» vs «not applicable»; рекомендация — избегать NULL, использовать домены и DEFAULT или отдельные таблицы.

**View updating problem:** не все VIEW обновляемы; JOIN view, aggregation view — неоднозначность какую base table обновлять. SQL1999+ CHECK OPTION, INSTEAD OF triggers; PostgreSQL — rules, triggers.

**Duplicate rows:** SQL bag semantics (multiset) vs relational set; DISTINCT «латание».

**Foreign key actions:** theory vs CASCADE практика.

**The Third Manifesto / Tutorial D:** альтернатива SQL (не промышленный стандарт, но учит мыслить реляционно).

**PostgreSQL:** близок к SQL standard, но extensions (JSONB, arrays) — pragmatic departure.

Читать: Date «SQL and Relational Theory», главы о NULL, views, constraints.

### Что читать в источниках

1. **1-я очередь.** К. Дж. Дейт — Введение в системы баз данных (8-е изд.) — Главы 19–21
2. **2-я очередь.** К. Дж. Дейт — SQL и реляционная теория — Главы 11–14
### Ключевые понятия

- **NULL problem** — трёхзначная логика.
- **View updating** — обновление представлений.
- **Bag vs set** — дубликаты в SQL.
- **Relational fidelity** — соответствие теории.

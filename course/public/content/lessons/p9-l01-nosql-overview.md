## NoSQL: обзор моделей и сценариев

**Часть:** Альтернативные СУБД и итоговая аттестация · **Модуль:** NoSQL и графовые БД

Фокус на теории и тесте; SQL не обязателен.

### Цели урока

- Классифицировать document, key-value, graph, column
- Сопоставить NoSQL и реляционные БД
- Выбрать технологию под use case

### Краткая теория

**NoSQL** — не «no SQL», а «not only SQL»; отказ от строгой relational модели ради scale/flexibility.

| Модель | Пример | Use case |
|--------|--------|----------|
| Document | MongoDB | JSON catalog, CMS |
| Key-value | Redis | Cache, sessions |
| Column-family | Cassandra | Time series, wide rows |
| Graph | Neo4j | Social, fraud, paths |

**vs RDBMS:** схема гибкая vs rigid; horizontal scale vs vertical; eventual consistency vs ACID (часто); JOIN expensive vs normalized.

**Когда PostgreSQL достаточно:** JSONB + GIN, pgvector, ltree — «SQL + extensions».

**Когда MongoDB:** nested documents, rapid schema change, shard by access pattern.

**Когда Graph:** many-hop relationships (friends-of-friends), shortest path — JOIN hell в SQL.

### Что читать в источниках

1. **1-я очередь.** Брэдшоу, Брэзил, Ходоров — MongoDB: полное руководство — Глава 1
2. **2-я очередь.** Robinson, Webber, Eifrem — Graph Databases (2nd ed.) — Глава 1
### Ключевые понятия

- **Document DB** — JSON/BSON documents.
- **Key-value** — K-V store.
- **Graph DB** — vertices and edges.
- **CAP** — trade-offs at scale.

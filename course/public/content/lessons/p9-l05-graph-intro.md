## Графовые базы данных: модель и применение

**Часть:** Альтернативные СУБД и итоговая аттестация · **Модуль:** NoSQL и графовые БД

Фокус на теории и тесте; SQL не обязателен.

### Цели урока

- Определить вершины, рёбра и свойства
- Привести примеры social и fraud graphs
- Оценить преимущества перед RDBMS

### Краткая теория

**Property Graph:** **vertices (nodes)** + **edges (relationships)** + properties on both.

Примеры:
- **Social:** Person —FRIEND→ Person; recommendation, communities.
- **Fraud:** Account —TRANSFER→ Account; cycle detection, mule networks.
- **University:** Student —ENROLLED→ Course —TAUGHT_BY→ Teacher; prerequisites chain.

**vs RDBMS:** recursive CTE в SQL для graphs возможен, но multi-hop (6+) дорог (JOIN explosion). Graph DB: **index-free adjacency**, native traversal O(edges) not O(rows).

**Neo4j, Amazon Neptune, etc.** — Cypher, Gremlin query languages.

**When not graph:** simple FK relationships, reporting aggregates — PostgreSQL достаточно.

### Что читать в источниках

1. **1-я очередь.** Комаров В. И. — Путеводитель по базам данных — Раздел 17: graph DB
2. **2-я очередь.** Robinson, Webber, Eifrem — Graph Databases (2nd ed.) — Главы 2–3
### Ключевые понятия

- **Vertex** — узел графа.
- **Edge** — relationship.
- **Traversal** — обход графа.
- **Index-free adjacency** — быстрый local hop.

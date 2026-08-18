## Graph DB: Cypher и обход графа

**Часть:** Альтернативные СУБД и итоговая аттестация · **Модуль:** NoSQL и графовые БД

Фокус на теории и тесте; SQL не обязателен.

### Цели урока

- Написать MATCH и RETURN в Cypher
- Выполнить k-hop обход
- Сравнить производительность с JOIN

### Краткая теория

**Cypher (Neo4j):**

```cypher
MATCH (s:Student {name: 'Иванов'})-[:ENROLLED]->(c:Course)
RETURN c.name, c.credits

MATCH (a:Person)-[:FRIEND*1..3]-(b:Person)
WHERE a.name = 'Alice'
RETURN DISTINCT b.name

MATCH path = (s:Student)-[:PREREQ*]->(c:Course {name: 'БД'})
RETURN path
```

**k-hop:** variable length `[*1..k]` — друзья до 3 уровня.

**vs SQL:**
```sql
WITH RECURSIVE hops AS (
  SELECT friend_id, 1 AS depth FROM friends WHERE user_id = 1
  UNION ALL
  SELECT f.friend_id, h.depth+1 FROM friends f JOIN hops h ON f.user_id = h.friend_id WHERE h.depth < 3
) SELECT * FROM hops;
```

Graph wins on deep/varied traversals; SQL wins on aggregates over star schema.

Опционально: [Neo4j Browser sandbox](https://sandbox.neo4j.com) без локальной установки.

### Что читать в источниках

1. **1-я очередь.** Брэдшоу, Брэзил, Ходоров — MongoDB: полное руководство — Глава 7 (сравнение)
2. **2-я очередь.** Robinson, Webber, Eifrem — Graph Databases (2nd ed.) — Главы 4–5
### Ключевые понятия

- **Cypher** — язык запросов Neo4j.
- **MATCH** — pattern matching.
- **Variable-length path** — k-hop traversal.

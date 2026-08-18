## MongoDB: aggregation pipeline

**Часть:** Альтернативные СУБД и итоговая аттестация · **Модуль:** NoSQL и графовые БД

Фокус на теории и тесте; SQL не обязателен.

### Цели урока

- Построить pipeline $match, $group, $lookup
- Сформировать аналитический отчёт
- Сравнить с SQL GROUP BY

### Краткая теория

**Aggregation pipeline** — stages left-to-right:

```javascript
db.performance.aggregate([
  { $match: { year: 2025 } },
  { $group: { _id: "$group", avgGrade: { $avg: "$grade" } } },
  { $sort: { avgGrade: -1 } },
  { $lookup: { from: "groups", localField: "_id", foreignField: "code", as: "g" } }
])
```

**Stages:** $match (filter), $group (aggregate), $project, $lookup (left join), $unwind (flatten array).

**SQL equivalent:**
```sql
SELECT group_id, avg(grade) FROM performance WHERE year=2025 GROUP BY group_id ORDER BY 2 DESC;
-- $lookup ≈ LEFT JOIN
```

Для DWH-grade analytics часто проще SQL/star schema; Mongo aggregation — когда data already in documents.

> **Опционально:** задания можно выполнить на [MongoDB Playground](https://mongoplayground.net) без локальной установки.

### Что читать в источниках

1. **1-я очередь.** Линн Бейли — Изучаем SQL — Приложение: NoSQL
2. **2-я очередь.** Брэдшоу, Брэзил, Ходоров — MongoDB: полное руководство — Глава 6
### Ключевые понятия

- **$match** — filter stage.
- **$group** — aggregation.
- **$lookup** — join-like stage.

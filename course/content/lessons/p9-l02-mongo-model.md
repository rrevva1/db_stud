## MongoDB: документная модель и BSON

**Часть:** Альтернативные СУБД и итоговая аттестация · **Модуль:** NoSQL и графовые БД

Фокус на теории и тесте; SQL не обязателен.

### Цели урока

- Описать коллекции и документы
- Спроектировать вложенную схему
- Сравнить embedding и referencing

### Краткая теория

**MongoDB:** database → **collection** → **document** (BSON). Нет фиксированной схемы (flexible schema).

```json
{
  "_id": ObjectId("..."),
  "student_id": 101,
  "name": "Иванов",
  "group": { "code": "ИВТ-21", "faculty": "IT" },
  "grades": [ { "subject": "БД", "score": 5 } ]
}
```

**Embedding** — вложенные массивы/объекты: один read, atomic update документа; но document size limit 16MB, duplication.

**Referencing** — `$lookup` или manual refs like SQL FK: normalization, smaller docs; нужны доп. queries.

**vs PostgreSQL JSONB:** Mongo — native sharding, aggregation pipeline; PG — ACID, JOIN, один стек.

> **Опционально:** задания можно выполнить на [MongoDB Playground](https://mongoplayground.net) без локальной установки.

### Что читать в источниках

1. **1-я очередь.** Комаров В. И. — Путеводитель по базам данных — Раздел 16: document DB
2. **2-я очередь.** Брэдшоу, Брэзил, Ходоров — MongoDB: полное руководство — Главы 2–3
### Ключевые понятия

- **Collection** — набор документов.
- **BSON** — binary JSON.
- **Embedding** — вложение данных.
- **Referencing** — ссылки между docs.

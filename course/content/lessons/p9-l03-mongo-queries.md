## MongoDB: CRUD и запросы

**Часть:** Альтернативные СУБД и итоговая аттестация · **Модуль:** NoSQL и графовые БД

Фокус на теории и тесте; SQL не обязателен.

### Цели урока

- Выполнить find, insert, update, delete
- Использовать операторы $gt, $in, $regex
- Создать индексы в MongoDB

### Краткая теория

**CRUD (MongoDB shell / driver):**

```javascript
db.students.insertOne({ name: "Петров", group: "ИВТ-21" })
db.students.find({ "grades.score": { $gt: 4 } })
db.students.updateOne({ name: "Петров" }, { $set: { status: "active" } })
db.students.deleteMany({ status: "inactive" })
```

**Operators:** `$gt`, `$gte`, `$in`, `$regex`, `$elemMatch`.

**Indexes:** `db.students.createIndex({ group: 1, name: 1 })`

**PostgreSQL equivalent:**

| Mongo | PostgreSQL |
|-------|------------|
| find({a:1}) | SELECT * WHERE a=1 |
| $gt | > |
| $in | IN (...) |
| insertOne | INSERT ... RETURNING |
| updateOne $set | UPDATE ... SET |

> **Опционально:** задания можно выполнить на [MongoDB Playground](https://mongoplayground.net) без локальной установки.

### Что читать в источниках

1. **1-я очередь.** Братусь Н. В. и др. — Базы данных. Практикум — Задание 9: MongoDB
2. **2-я очередь.** Брэдшоу, Брэзил, Ходоров — MongoDB: полное руководство — Главы 4–5
### Ключевые понятия

- **find** — query documents.
- **$operators** — filter operators.
- **createIndex** — index in Mongo.

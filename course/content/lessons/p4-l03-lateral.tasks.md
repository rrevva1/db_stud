## Практика PostgreSQL

### Задание 1. TOP-2 оценки по предметам

Для каждого `subject` выведите двух лучших студентов с оценками. Используйте `CROSS JOIN LATERAL` с `ORDER BY grade DESC LIMIT 2`.

### Задание 2. unnest тегов

Таблица `article(id, title, tags text[])`. Разверните теги в строки с сохранением порядка (`WITH ORDINALITY`).

### Задание 3. JSON-массив позиций заказа

```sql
CREATE TABLE order_demo (
    id serial PRIMARY KEY,
    items jsonb
);
INSERT INTO order_demo (items) VALUES
  ('[{"sku":"A1","qty":2},{"sku":"B3","qty":1}]');
```

Извлеките `sku` и `qty` через `jsonb_array_elements` и `LATERAL`.

### Задание 4. LEFT JOIN LATERAL

Выведите все группы и **если есть** трёх лучших студентов; для пустых групп — одну строку с NULL в полях студента.

### Самопроверка

- [ ] Подзапрос в LATERAL ссылается на столбцы «слева»
- [ ] LIMIT внутри LATERAL ограничивает строки **на группу**
- [ ] unnest не теряет связь с id родительской строки

Сохраните: `course/sql/p4-l03-lateral-solution.sql`

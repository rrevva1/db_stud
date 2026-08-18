## Снежинка (Snowflake Schema)

**Часть:** Хранилища данных · **Модуль:** DWH и dimensional modeling

Фокус на теории и тесте; SQL не обязателен.

### Цели урока

- Нормализовать измерения в snowflake
- Сравнить star и snowflake
- Выбрать схему для ETL

### Краткая теория

**Snowflake** — dimensions **нормализованы** в иерархии:

```
dim_group → dim_faculty → dim_university
fact → dim_student → dim_group → ...
```

**Star vs Snowflake:**

| | Star | Snowflake |
|---|------|-----------|
| Dimensions | Flat wide | Normalized chains |
| JOIN count | Меньше | Больше |
| Storage | Больше redundancy | Меньше |
| ETL | Проще load wide | Сложнее maintain FKs |
| BI tools | Предпочитают star | Extra joins |

Для **университета:** snowflake если faculty/university shared across marts и нужна строгая конformность; star — если скорость разработки важнее.

Kimball: обычно star; snowflake — когда dimensions очень большие или shared conformed dimensions (Inmon bus).

### Что читать в источниках

1. **1-я очередь.** Комаров В. И. — Путеводитель по базам данных — Раздел 15: snowflake
2. **2-я очередь.** Смирнов М. В. — Проектирование хранилищ данных — Глава 4, §4.2
### Ключевые понятия

- **Snowflake schema** — нормализованные dimensions.
- **Conformed dimension** — общее измерение.
- **Hierarchy** — faculty → university.

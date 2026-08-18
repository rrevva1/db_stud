## Кейс: проектирование хранилища продаж

**Часть:** Хранилища данных · **Модуль:** DWH и dimensional modeling

Лабораторная. Среда: **PostgreSQL**.

### Цели урока

- Построить star schema для retail
- Написать ETL-скрипт загрузки
- Сформировать аналитический отчёт

### Краткая теория

**Лабораторная:** retail sales DWH (Smirnov практика) + параллельно **university star** из p8-l03.

**Retail star:**
- fact_sales (sale_id grain): quantity, amount, discount
- dim_product, dim_customer, dim_store, dim_date

**ETL sketch (PostgreSQL staging):**
```sql
CREATE TABLE stg_sales AS SELECT * FROM oltp.sales WHERE sale_date >= current_date - 1;
INSERT INTO fact_sales SELECT ... surrogate lookups ... FROM stg_sales;
```

**Отчёт:** выручка по магазинам и категориям за месяц.

**University extension:** fact_grade + dims; отчёт — топ-5 групп по среднему баллу.

### Что читать в источниках

1. **1-я очередь.** Братусь Н. В. и др. — Базы данных. Практикум — Задание 8: DWH
2. **2-я очередь.** Смирнов М. В. — Проектирование хранилищ данных — Глава 8 (практика)
### Ключевые понятия

- **Retail star** — fact_sales.
- **ETL script** — staging to fact.
- **BI report** — GROUP BY aggregates.

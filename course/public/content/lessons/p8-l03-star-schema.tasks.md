## Задания — проектирование star schema университета

**Обязательное задание:** спроектируйте star schema для аналитики успеваемости.

1. **Fact table** `fact_grade` — определите grain и measures (grade, credits, is_pass).
2. **Dimensions:** `dim_student`, `dim_group`, `dim_subject`, `dim_date`, `dim_department`.
3. Для каждой dimension перечислите 5+ атрибутов (denormalized где нужно).
4. Нарисуйте диаграмму звезды (draw.io).
5. Напишите SQL-запрос: средний балл по кафедрам за 2024–2025 уч. год.
6. Обоснуйте выбор grain и surrogate keys.

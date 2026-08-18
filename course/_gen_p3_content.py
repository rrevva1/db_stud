# -*- coding: utf-8 -*-
"""Generate Part 3 lesson content (Russian, PostgreSQL). UTF-8 without BOM."""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from _gen_p3_theory import THEORY
from _gen_p3_quizzes import QUIZZES
from _gen_p3_tasks import TASKS
from _gen_p3_sql import (
    SCHEMA_UNIVERSITY,
    SQL_CREATE_TABLES,
    SQL_INSERT_SELECT,
    SQL_DATA_TYPES,
    SQL_CONSTRAINTS,
    SQL_JOINS,
    SQL_GROUP_BY,
    SQL_SUBQUERIES,
    SQL_LAB_UNIVERSITY,
)

LESSONS = os.path.join(BASE, "content", "lessons")
SQL_DIR = os.path.join(BASE, "sql")

LESSON_META = [
    ("p3-l01-create-table", "CREATE TABLE: создание таблиц и схем", "DDL: определение структуры",
     ["Создать таблицу с именованными столбцами", "Использовать схемы для организации объектов", "Применить IF NOT EXISTS и комментарии"],
     [("morgunov", "Глава 3, §3.1"), ("headfirst", "Глава 5")]),
    ("p3-l02-data-types", "Типы данных PostgreSQL", "DDL: определение структуры",
     ["Выбрать подходящие типы для атрибутов", "Использовать serial, numeric, timestamp", "Понять различия text и varchar"],
     [("morgunov", "Глава 3, §3.2"), ("novikov", "Глава 8, §8.1")]),
    ("p3-l03-constraints", "Ограничения: PRIMARY KEY, FOREIGN KEY, CHECK, UNIQUE", "DDL: определение структуры",
     ["Задать первичный и внешний ключи", "Добавить CHECK и UNIQUE ограничения", "Обработать ошибки нарушения целостности"],
     [("morgunov", "Глава 3, §3.3"), ("practicum", "Глава 4: ограничения")]),
    ("p3-l04-alter-table", "ALTER TABLE: изменение структуры", "DDL: определение структуры",
     ["Добавить и удалить столбцы", "Изменить тип данных и ограничения", "Переименовать таблицы и столбцы"],
     [("morgunov", "Глава 3, §3.4"), ("headfirst", "Глава 6")]),
    ("p3-l05-insert", "INSERT: добавление данных", "DML: изменение данных",
     ["Вставить одну и несколько строк", "Использовать INSERT … RETURNING", "Загрузить данные из SELECT"],
     [("morgunov", "Глава 4, §4.1"), ("headfirst", "Глава 7")]),
    ("p3-l06-update", "UPDATE: изменение данных", "DML: изменение данных",
     ["Обновить строки по условию", "Использовать UPDATE … FROM", "Предотвратить нежелательные массовые обновления"],
     [("morgunov", "Глава 4, §4.2"), ("practicum", "Задание 4: DML")]),
    ("p3-l07-delete", "DELETE и TRUNCATE", "DML: изменение данных",
     ["Удалить строки по условию", "Сравнить DELETE и TRUNCATE", "Учесть каскадное удаление"],
     [("morgunov", "Глава 4, §4.3"), ("headfirst", "Глава 8")]),
    ("p3-l08-select-basics", "SELECT: базовый синтаксис запросов", "SELECT и соединения",
     ["Выбрать столбцы и задать псевдонимы", "Использовать DISTINCT", "Ограничить результат LIMIT/OFFSET"],
     [("morgunov", "Глава 5, §5.1"), ("headfirst", "Глава 9")]),
    ("p3-l09-where-order", "WHERE, ORDER BY и операторы сравнения", "SELECT и соединения",
     ["Фильтровать строки сложными условиями", "Сортировать по нескольким столбцам", "Применять BETWEEN, IN, LIKE"],
     [("morgunov", "Глава 5, §5.2"), ("practicum", "Глава 5: фильтрация")]),
    ("p3-l10-joins-intro", "Соединения таблиц: обзор и синтаксис", "SELECT и соединения",
     ["Объяснить необходимость JOIN", "Записать условие соединения ON/USING", "Отличить INNER от OUTER JOIN"],
     [("morgunov", "Глава 6, §6.1"), ("headfirst", "Глава 10")]),
    ("p3-l11-inner-join", "INNER JOIN: пересечение данных", "SELECT и соединения",
     ["Соединить две и более таблиц", "Использовать составные ключи", "Оптимизировать читаемость запроса"],
     [("morgunov", "Глава 6, §6.2"), ("practicum", "Задание 5: соединения")]),
    ("p3-l12-outer-join", "LEFT, RIGHT и FULL OUTER JOIN", "SELECT и соединения",
     ["Сохранить строки без пары", "Обработать NULL при внешнем соединении", "Выбрать подходящий тип OUTER JOIN"],
     [("morgunov", "Глава 6, §6.3"), ("headfirst", "Глава 11")]),
    ("p3-l13-cross-self-join", "CROSS JOIN и SELF JOIN", "SELECT и соединения",
     ["Построить декартово произведение", "Применить самосоединение для иерархий", "Оценить риски CROSS JOIN"],
     [("morgunov", "Глава 6, §6.4"), ("novikov", "Глава 5, §5.3")]),
    ("p3-l14-group-by", "GROUP BY и агрегирование", "Агрегация и подзапросы",
     ["Группировать данные по столбцам", "Использовать COUNT, SUM, AVG, MIN, MAX", "Понять правило «все столбцы в GROUP BY»"],
     [("morgunov", "Глава 7, §7.1"), ("headfirst", "Глава 12")]),
    ("p3-l15-having", "HAVING: фильтрация групп", "Агрегация и подзапросы",
     ["Отличить WHERE от HAVING", "Фильтровать агрегированные результаты", "Комбинировать GROUP BY и HAVING"],
     [("morgunov", "Глава 7, §7.2"), ("practicum", "Задание 6: агрегаты")]),
    ("p3-l16-subqueries", "Подзапросы: scalar, IN, EXISTS", "Агрегация и подзапросы",
     ["Вложить SELECT во WHERE и FROM", "Использовать EXISTS для проверки наличия", "Сравнить подзапросы и JOIN"],
     [("morgunov", "Глава 8, §8.1"), ("headfirst", "Глава 13")]),
    ("p3-l17-set-ops", "Операции над множествами: UNION, INTERSECT, EXCEPT", "Агрегация и подзапросы",
     ["Объединить результаты запросов", "Убрать дубликаты UNION ALL", "Применить INTERSECT и EXCEPT"],
     [("morgunov", "Глава 8, §8.2"), ("date-sql", "Глава 5")]),
    ("p3-l18-scalar-funcs", "Скalarные функции и выражения", "Функции, транзакции и объекты БД",
     ["Использовать строковые и числовые функции", "Работать с датами и интервалами", "Применять COALESCE и NULLIF"],
     [("morgunov", "Глава 9, §9.1"), ("headfirst", "Глава 14")]),
    ("p3-l19-case-when", "Условные выражения CASE и CAST", "Функции, транзакции и объекты БД",
     ["Построить ветвление CASE WHEN", "Приводить типы CAST и ::", "Создать вычисляемые столбцы"],
     [("morgunov", "Глава 9, §9.2"), ("practicum", "Глава 6: выражения")]),
    ("p3-l20-transactions", "Транзакции: BEGIN, COMMIT, ROLLBACK", "Функции, транзакции и объекты БД",
     ["Оформить операции в транзакцию", "Откатить изменения при ошибке", "Понять свойства ACID"],
     [("morgunov", "Глава 10, §10.1"), ("novikov", "Глава 9, §9.2")]),
    ("p3-l21-isolation", "Уровни изоляции и аномалии параллелизма", "Функции, транзакции и объекты БД",
     ["Настроить READ COMMITTED и REPEATABLE READ", "Распознать dirty read и phantom read", "Выбрать уровень изоляции для задачи"],
     [("morgunov", "Глава 10, §10.2"), ("date-intro", "Глава 16")]),
    ("p3-l22-views", "Представления (VIEW) и материализованные представления", "Функции, транзакции и объекты БД",
     ["Создать обычное и материализованное VIEW", "Обновлять данные через представления", "Применить REFRESH MATERIALIZED VIEW"],
     [("morgunov", "Глава 11, §11.1"), ("practicum", "Глава 7: представления")]),
    ("p3-l23-triggers", "Триггеры и хранимые функции PL/pgSQL", "Функции, транзакции и объекты БД",
     ["Создать BEFORE/AFTER триггер", "Написать простую функцию на PL/pgSQL", "Обеспечить аудит изменений"],
     [("morgunov", "Глава 11, §11.2"), ("novikov", "Глава 10, §10.3")]),
    ("p3-l24-exam", "Контроль: основы SQL и манипулирование данными", "Функции, транзакции и объекты БД",
     ["Написать DDL и DML для заданной схемы", "Построить запросы с JOIN и агрегатами", "Продемонстрировать работу с транзакциями"],
     [("morgunov", "Главы 3–11 (повторение)"), ("practicum", "Задания 4–7 (повторение)")]),
]


def write_utf8(path, content):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def make_header(title, module, objectives, sources):
    obj_lines = "\n".join(f"- {o}" for o in objectives)
    src_lines = "\n".join(f"- **{s[0]}**: {s[1]}" for s in sources)
    return f"""## {title}

**Часть:** SQL: язык манипулирования и определения данных · **Модуль:** {module}

Практика выполняется в **PostgreSQL** (psql или pgAdmin). Сквозная предметная область — **университет** (студенты, группы, оценки).

### Цели урока

{obj_lines}

### Что читать в источниках

{src_lines}

"""


def generate_sql_files():
    files = {
        "schema-university.sql": SCHEMA_UNIVERSITY,
        "p3-l01-create-tables.sql": SQL_CREATE_TABLES,
        "p3-l02-insert-select.sql": SQL_INSERT_SELECT,
        "p3-l04-data-types.sql": SQL_DATA_TYPES,
        "p3-l06-ddl-constraints.sql": SQL_CONSTRAINTS,
        "p3-l14-joins.sql": SQL_JOINS,
        "p3-l17-group-by.sql": SQL_GROUP_BY,
        "p3-l19-subqueries.sql": SQL_SUBQUERIES,
        "p3-l22-lab-university.sql": SQL_LAB_UNIVERSITY,
    }
    os.makedirs(SQL_DIR, exist_ok=True)
    for name, content in files.items():
        write_utf8(os.path.join(SQL_DIR, name), content)
    return files


def main():
    os.makedirs(LESSONS, exist_ok=True)
    count = 0
    for lid, title, module, objectives, sources in LESSON_META:
        header = make_header(title, module, objectives, sources)
        body = THEORY.get(lid, "### Краткая теория\n\nСм. источники.\n")
        write_utf8(os.path.join(LESSONS, f"{lid}.md"), header + body)
        count += 1

        quiz = QUIZZES.get(lid, [])
        write_utf8(
            os.path.join(LESSONS, f"{lid}.quiz.json"),
            json.dumps({"lessonId": lid, "passingScore": 70, "questions": quiz},
                       ensure_ascii=False, indent=2),
        )
        count += 1

        tasks = TASKS.get(lid, f"## Практика PostgreSQL\n\nЗадания по теме «{title}».\n")
        write_utf8(os.path.join(LESSONS, f"{lid}.tasks.md"), tasks)
        count += 1

    count += len(generate_sql_files())
    print(f"WRITTEN: {count}")


if __name__ == "__main__":
    main()

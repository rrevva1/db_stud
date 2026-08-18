# Дампы учебных баз данных

Готовые схемы для переноса на другую машину. Обе живут в одной PostgreSQL-базе `dbstud` (разные схемы `university` и `airline`).

## Восстановление из SQL

```bash
createdb dbstud   # если базы ещё нет
psql -d dbstud -f dumps/university.sql
psql -d dbstud -f dumps/airline.sql
```

Windows (PowerShell):

```powershell
createdb dbstud
psql -d dbstud -f dumps/university.sql
psql -d dbstud -f dumps/airline.sql
```

## Файлы

| Файл | Содержимое |
|------|------------|
| `university.sql` | Схема university + факультеты, группы, студенты, оценки |
| `airline.sql` | Схема airline + аэропорты, рейсы, бронирования |
| `university.dump` | `pg_dump -Fc` (если собран на машине с PostgreSQL) |
| `airline.dump` | то же для airline |

## Сборка custom dump (опционально)

После загрузки SQL:

```bash
pg_dump -d dbstud -n university -Fc -f dumps/university.dump
pg_dump -d dbstud -n airline -Fc -f dumps/airline.dump
```

Восстановление из `.dump`:

```bash
pg_restore -d dbstud --clean --if-exists dumps/university.dump
pg_restore -d dbstud --clean --if-exists dumps/airline.dump
```

Исходники скриптов практики: [`course/sql/`](../course/sql/).

# Курс «Базы данных: от проектирования до SQL»

Локальное веб-приложение в формате Stepik: **теория → источники (PDF) → тест → практика**.

## Быстрый старт (без Node.js)

1. Откройте терминал в папке `course`:
   ```powershell
   cd e:\Projects\db_stud\course
   python -m http.server 8080
   ```
2. В браузере откройте: **http://localhost:8080/static/**

Прогресс сохраняется в `localStorage` браузера.

## Запуск с Vite + React (если установлен Node.js)

```powershell
cd e:\Projects\db_stud\course
npm install
npm run dev
```

Откроется http://localhost:5173

Сборка production:
```powershell
npm run build
npm run preview
```

## Структура

| Путь | Назначение |
|------|------------|
| `content/` | Данные курса: `curriculum.json`, `sources.json`, `coverage.json`, `lessons/` |
| `public/content/` | Копия для статической раздачи (синхронизируется скриптом) |
| `static/` | Просмотрщик без сборки (HTML + JS) |
| `src/` | React-приложение (Vite) |
| `sql/` | Эталонные SQL-скрипты для практики |

После правок в `content/` синхронизируйте:
```powershell
Copy-Item -Recurse -Force content\* public\content\
```

## Программа

- **105 уроков** в 10 частях (0–9)
- Ядро: проектирование (лекция 1) + SQL PostgreSQL (Моргунов + практикум)
- Практика SQL — только **PostgreSQL**; T-SQL/MongoDB — отдельные ветки с пометкой диалекта
- Сквозные схемы: **университет** (`sql/schema-university.sql`) и **авиакомпания** (`sql/schema-airline.sql`)
- Литература: [`../sources/`](../sources/README.md) (Автор — Название)
- Дампы для переноса БД: [`../dumps/`](../dumps/README.md)

## PostgreSQL

Установите PostgreSQL 16, создайте БД `dbstud`. Восстановление готовых схем:

```bash
psql -d dbstud -f ../dumps/university.sql
psql -d dbstud -f ../dumps/airline.sql
```

Либо выполняйте скрипты из `sql/` по заданиям уроков.

Подробный план курса: [`../docs/COURSE_PLAN.md`](../docs/COURSE_PLAN.md)

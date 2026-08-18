## Практика PostgreSQL

### Задание 1. Универсальный отчёт

Функция `search_bookings(p_from date, p_to date, p_status text DEFAULT NULL)` — динамический WHERE, все значения через USING.

### Задание 2. Whitelist сортировки

Параметр `p_order_by` только из `('booked_at','amount','id')`. Иначе `RAISE EXCEPTION`.

### Задание 3. PREPARE

PREPARE/EXECUTE/DEALLOCATE для частого INSERT в лог.

### Задание 4. SECURITY DEFINER (разбор)

Создайте функцию DEFINER с `SET search_path = pg_catalog, public`. Объясните, что сломается без этого.

### Задание 5. Атака (учебная)

Покажите небезопасную функцию с конкатенацией и исправленную версию. **Только на тестовой БД.**

### Самопроверка

- [ ] Whitelist для имён столбцов/таблиц
- [ ] search_path зафиксирован в DEFINER
- [ ] Нет %s с внешним вводом

Сохраните: `course/sql/p5-l09-dynamic-advanced-solution.sql`

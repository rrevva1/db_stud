## Аутентификация и pg_hba.conf

**Часть:** Администрирование и архитектуры нагрузок · **Модуль:** Безопасность и эксплуатация

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Настроить методы аутентификации
- Редактировать pg_hba.conf
- Подключиться с SSL-сертификатом

### Краткая теория

**Аутентификация** — кто вы; **авторизация** — что вам можно (GRANT, RLS).

**pg_hba.conf** — правила подключения (Host-Based Authentication):

```
// TYPE  DATABASE  USER  ADDRESS       METHOD
local   all       all                 peer
host    mydb      app   10.0.0.0/24   scram-sha-256
hostssl all       all   0.0.0.0/0     cert
```

Методы: **trust**, **peer** (local), **md5/scram-sha-256**, **cert** (SSL client cert).

После изменения: `pg_ctl reload` или `SELECT pg_reload_conf();`

**SSL in transit:** `ssl=on`, сертификаты в postgresql.conf; клиент `sslmode=verify-full`.

Роли ≠ пользователи ОС: `CREATE ROLE app_user LOGIN PASSWORD '...';`

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 21, §21.1
2. **2-я очередь.** Новиков Б. А. и др. — Основы технологий баз данных — Глава 15, §15.1
### Ключевые понятия

- **pg_hba.conf** — правила аутентификации.
- **SCRAM-SHA-256** — современный hash пароля.
- **sslmode** — режим SSL клиента.

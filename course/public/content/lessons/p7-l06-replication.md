## Репликация: streaming и logical

**Часть:** Администрирование и архитектуры нагрузок · **Модуль:** Безопасность и эксплуатация

Практика: **PostgreSQL** (psql или pgAdmin).

### Цели урока

- Настроить streaming replication
- Объяснить logical replication
- Спланировать failover

### Краткая теория

**Streaming (physical):** standby получает WAL потоком; побайтовая копия кластера.

Primary: `wal_level=replica`, `max_wal_senders`, replication role.
Standby: `primary_conninfo`, `hot_standby=on`.

**Logical replication:** публикация/подписка на уровне таблиц; cross-version, selective.

```sql
CREATE PUBLICATION pub_perf FOR TABLE performance;
CREATE SUBSCRIPTION sub_perf CONNECTION '...' PUBLICATION pub_perf;
```

**Failover:** Patroni, repmgr, manual promote. **CAP:** при partition сеть — выбор CP vs AP (PostgreSQL sync rep → CP bias).

**Read replicas:** отчёты на standby, снижение нагрузки на primary (OLAP на replica).

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 22, §22.2
2. **2-я очередь.** Новиков Б. А. и др. — Основы технологий баз данных — Глава 16, §16.1
### Ключевые понятия

- **Streaming replication** — физическая WAL-репликация.
- **Logical replication** — табличная публикация.
- **Standby** — реplica-сервер.
- **Failover** — переключение primary.

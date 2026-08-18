# -*- coding: utf-8 -*-
# Part 2: lessons p7-p9 (exec'd into enhance_p6_p9.py)

# ===== PART 7 =====
LESSONS["p7-l01-auth"] = {
"md": md("Аутентификация и pg_hba.conf", P7, M7, SQL,
    ["Настроить методы аутентификации", "Редактировать pg_hba.conf", "Подключиться с SSL-сертификатом"],
    """**Аутентификация** — кто вы; **авторизация** — что вам можно (GRANT, RLS).

**pg_hba.conf** — правила подключения (Host-Based Authentication):

```
# TYPE  DATABASE  USER  ADDRESS       METHOD
local   all       all                 peer
host    mydb      app   10.0.0.0/24   scram-sha-256
hostssl all       all   0.0.0.0/0     cert
```

Методы: **trust**, **peer** (local), **md5/scram-sha-256**, **cert** (SSL client cert).

После изменения: `pg_ctl reload` или `SELECT pg_reload_conf();`

**SSL in transit:** `ssl=on`, сертификаты в postgresql.conf; клиент `sslmode=verify-full`.

Роли ≠ пользователи ОС: `CREATE ROLE app_user LOGIN PASSWORD '...';`""",
    [("morgunov", "Глава 21, §21.1"), ("novikov", "Глава 15, §15.1")],
    [("pg_hba.conf", "правила аутентификации"), ("SCRAM-SHA-256", "современный hash пароля"),
     ("sslmode", "режим SSL клиента")]),
"quiz": quiz("p7-l01-auth",
    sq("q1", "pg_hba.conf определяет…", ["Правила подключения", "План JOIN", "TOAST", "ETL"], 0, "HBA rules."),
    sq("q2", "scram-sha-256 — это…", ["Метод аутентификации", "Тип индекса", "WAL level", "OLAP cube"], 0, "Password auth."),
    sq("q3", "hostssl требует…", ["SSL-соединение", "Local socket only", "No password", "MongoDB"], 0, "Encrypted transport."),
    sq("q4", "После правки pg_hba…", ["pg_reload_conf()", "DROP DATABASE", "VACUUM FULL", "CREATE EXTENSION"], 0, "Reload config."),
    mq("q5", "Методы auth? (верные)", ["peer", "scram-sha-256", "cert", "hash join"], [0,1,2], "Auth methods.")),
"tasks": """## Практика PostgreSQL

1. Найдите pg_hba.conf (`SHOW hba_file;`).
2. Создайте роль `readonly` с LOGIN.
3. Добавьте правило (в тестовой среде) для scram-sha-256.
4. Опишите sslmode=verify-full vs require.""",
}

LESSONS["p7-l02-roles"] = {
"md": md("Роли, привилегии GRANT и REVOKE", P7, M7, SQL,
    ["Создать роли и назначить права", "Ограничить доступ к схемам и таблицам", "Применить принцип наименьших привилегий"],
    """PostgreSQL: **ROLE** = пользователь или группа. `CREATE ROLE`, `GRANT`, `REVOKE`.

```sql
CREATE ROLE analyst NOLOGIN;
GRANT CONNECT ON DATABASE university TO analyst;
GRANT USAGE ON SCHEMA public TO analyst;
GRANT SELECT ON student, s_group TO analyst;
GRANT analyst TO user_ivan;  -- membership
REVOKE INSERT ON performance FROM analyst;
```

**Привилегии:** SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER, CREATE, USAGE.

**Схемы:** `GRANT USAGE ON SCHEMA` — вход в схему; затем права на объекты.

**Default privileges:** `ALTER DEFAULT PRIVILEGES` для будущих таблиц.

**Least privilege:** приложению — только нужные DML; DBA — отдельная роль; не использовать superuser в app.""",
    [("morgunov", "Глава 21, §21.2"), ("petkovic", "Глава 9: безопасность")],
    [("GRANT", "выдача прав"), ("REVOKE", "отзыв прав"), ("ROLE", "пользователь/группа"),
     ("Least privilege", "минимально необходимые права")]),
"quiz": quiz("p7-l02-roles",
    sq("q1", "GRANT SELECT ON t TO r даёт…", ["Чтение таблицы t роли r", "INSERT", "Superuser", "WAL admin"], 0, "SELECT privilege."),
    sq("q2", "NOLOGIN роль…", ["Групповая роль", "Superuser only", "Cannot GRANT", "MongoDB role"], 0, "Group role pattern."),
    sq("q3", "USAGE ON SCHEMA нужен для…", ["Доступа к объектам схемы", "Backup", "Replication", "TOAST"], 0, "Schema access."),
    sq("q4", "Least privilege означает…", ["Минимум прав для задачи", "ALL PRIVILEGES всем", "Trust auth", "No RLS"], 0, "Security principle."),
    mq("q5", "Привилегии таблицы? (верные)", ["SELECT", "INSERT", "UPDATE", "MERGE only Mongo"], [0,1,2], "Table privileges.")),
"tasks": """## Практика PostgreSQL

1. CREATE ROLE app_read NOLOGIN; GRANT SELECT на student, s_group.
2. CREATE USER app1 LOGIN PASSWORD 'test'; GRANT app_read TO app1;
3. Проверьте: app1 может SELECT, не может INSERT.
4. REVOKE и проверка снова.""",
}

LESSONS["p7-l03-rls"] = {
"md": md("Row-Level Security (RLS)", P7, M7, SQL,
    ["Включить RLS на таблице", "Написать политику USING/WITH CHECK", "Протестировать изоляцию строк"],
    """**RLS** — фильтрация строк по политикам на уровне СУБД (не только в приложении).

```sql
ALTER TABLE performance ENABLE ROW LEVEL SECURITY;
CREATE POLICY perf_student ON performance
  FOR SELECT TO student_role
  USING (student_id = current_setting('app.student_id')::int);
CREATE POLICY perf_ins ON performance FOR INSERT TO student_role
  WITH CHECK (student_id = current_setting('app.student_id')::int);
```

**USING** — какие строки видны; **WITH CHECK** — какие можно вставить/обновить.

**BYPASSRLS** — атрибут роли (админ); **SECURITY DEFINER** функции — осторожно.

Сравнение с SQL Server: там тоже RLS (security predicates); в PostgreSQL — policies на таблице.""",
    [("morgunov", "Глава 21, §21.3"), ("pro-tsql", "Глава 15: RLS в SQL Server")],
    [("RLS", "безопасность на уровне строк"), ("USING", "фильтр чтения"),
     ("WITH CHECK", "ограничение записи"), ("Policy", "именованное правило")]),
"quiz": quiz("p7-l03-rls",
    sq("q1", "RLS включается…", ["ALTER TABLE ... ENABLE ROW LEVEL SECURITY", "CREATE INDEX", "VACUUM", "TOAST"], 0, "Enable RLS."),
    sq("q2", "USING определяет…", ["Видимые строки", "Только INSERT", "WAL level", "Backup"], 0, "Read filter."),
    sq("q3", "WITH CHECK для…", ["INSERT/UPDATE ограничений", "SELECT only", "DROP", "Replication"], 0, "Write filter."),
    sq("q4", "BYPASSRLS позволяет…", ["Обходить RLS", "Только read", "MongoDB sync", "FTS"], 0, "Admin bypass."),
    mq("q5", "RLS vs app filter? (верные)", ["RLS в СУБД", "Сложнее обойти", "Нужны policies", "Заменяет GRANT"], [0,1,2], "Defense in depth.")),
"tasks": """## Практика PostgreSQL

1. ENABLE RLS на performance для роли student.
2. Policy: студент видит только свои оценки (через session variable).
3. SET app.student_id; SELECT — проверка изоляции.
4. Сравните с RLS в SQL Server (pro-tsql ch.15).""",
}

LESSONS["p7-l04-encryption"] = {
"md": md("Шифрование: at rest и in transit", P7, M7, TH,
    ["Настроить SSL для подключений", "Объяснить TDE и pgcrypto", "Выбрать стратегию защиты данных"],
    """**In transit:** TLS между клиентом и PostgreSQL (`ssl=on`, `hostssl` в pg_hba). Защита от перехвата паролей/данных в сети.

**At rest:**
- **Файловая/дисковая** encryption (LUKS, BitLocker, cloud volume encryption) — прозрачно для PG.
- **TDE** (Transparent Data Encryption) — в SQL Server нативно; в PostgreSQL — через OS/disk или pg_tde extensions (сторонние).
- **pgcrypto** — шифрование столбцов: `pgp_sym_encrypt(data, key)`, хранение ciphertext.

```sql
CREATE EXTENSION pgcrypto;
INSERT INTO secrets(val) VALUES (pgp_sym_encrypt('text', 'key'));
SELECT pgp_sym_decrypt(val::bytea, 'key') FROM secrets;
```

**Ключи:** не в коде; vault/HSM; rotation policy.

**CAP-контекст:** шифрование не заменяет backup/replication; согласованность и доступность — отдельные оси.""",
    [("novikov", "Глава 15, §15.2"), ("komarov", "Раздел 14: шифрование")],
    [("TLS", "шифрование канала"), ("At rest", "шифрование на диске"),
     ("pgcrypto", "шифрование столбцов"), ("TDE", "прозрачное шифрование БД")]),
"quiz": quiz("p7-l04-encryption",
    sq("q1", "SSL/TLS защищает…", ["Данные in transit", "At rest only", "Только indexes", "WAL internal"], 0, "Network encryption."),
    sq("q2", "pgcrypto для…", ["Шифрования столбцов", "Hash join", "Replication", "VACUUM"], 0, "Column-level crypto."),
    sq("q3", "TDE в SQL Server…", ["Transparent disk encryption", "Only MongoDB", "No PostgreSQL analog native", "Both B and C partly true"], 3, "PG: OS/disk or extensions."),
    sq("q4", "Ключи шифрования…", ["Хранить в vault, не в коде", "В pg_hba.conf", "In plain SQL", "Public repo"], 0, "Key management."),
    mq("q5", "Defense layers? (верные)", ["TLS", "Disk encryption", "Column encrypt", "Disable auth"], [0,1,2], "Layered security.")),
"tasks": """## Задания

1. Опишите три уровня: TLS, disk encryption, pgcrypto column.
2. Когда column encryption vs disk encryption?
3. Сравните TDE SQL Server и подход PostgreSQL.
4. Риски хранения ключей в приложении.""",
}

LESSONS["p7-l05-backup"] = {
"md": md("Резервное копирование: pg_dump и pg_basebackup", P7, M7, SQL,
    ["Сделать логический дамп pg_dump", "Выполнить физический base backup", "Восстановить БД из резервной копии"],
    """**Логический backup — pg_dump:**
```bash
pg_dump -Fc -f university.dump university_db
pg_restore -d university_new university.dump
```
Портативный, выборочный; медленнее на huge DB.

**Физический — pg_basebackup:**
```bash
pg_basebackup -D /backup/base -Ft -z -P
```
Копия data directory + WAL для PITR. Требует wal_level=replica, replication slot.

**PITR:** archive_mode + restore_command → recovery до точки во времени.

**Стратегия:** RPO/RTO; ежедневный dump + continuous WAL archive; тест restore регулярно.

**pg_dump --schema-only** для DDL; **--data-only** для данных.""",
    [("morgunov", "Глава 22, §22.1"), ("petkovic", "Глава 10: backup")],
    [("pg_dump", "логический дамп"), ("pg_basebackup", "физическая копия"),
     ("PITR", "восстановление на момент времени"), ("RPO/RTO", "допустимая потеря/простой")]),
"quiz": quiz("p7-l05-backup",
    sq("q1", "pg_dump создаёт…", ["Логический дамп", "Physical only", "WAL segment", "MongoDB export"], 0, "Logical backup."),
    sq("q2", "pg_basebackup нужен wal_level…", ["replica или выше", "minimal only", "off", "Mongo"], 0, "For physical replication backup."),
    sq("q3", "PITR использует…", ["Base backup + WAL archive", "Only pg_dump", "Only TRUNCATE", "RLS"], 0, "Point-in-time recovery."),
    sq("q4", "pg_restore -d для…", ["Восстановления custom dump", "DELETE all", "CREATE USER", "ANALYZE"], 0, "Restore into DB."),
    mq("q5", "Backup best practices? (верные)", ["Test restore", "WAL archiving", "Offsite copy", "Never test"], [0,1,2], "Backup hygiene.")),
"tasks": """## Практика PostgreSQL

1. pg_dump -Fc вашей учебной БД.
2. pg_restore в новую БД test_restore.
3. Сравните размер custom vs plain SQL dump.
4. Опишите RPO/RTO для университета (оценки).""",
}

LESSONS["p7-l06-replication"] = {
"md": md("Репликация: streaming и logical", P7, M7, SQL,
    ["Настроить streaming replication", "Объяснить logical replication", "Спланировать failover"],
    """**Streaming (physical):** standby получает WAL потоком; побайтовая копия кластера.

Primary: `wal_level=replica`, `max_wal_senders`, replication role.
Standby: `primary_conninfo`, `hot_standby=on`.

**Logical replication:** публикация/подписка на уровне таблиц; cross-version, selective.

```sql
CREATE PUBLICATION pub_perf FOR TABLE performance;
CREATE SUBSCRIPTION sub_perf CONNECTION '...' PUBLICATION pub_perf;
```

**Failover:** Patroni, repmgr, manual promote. **CAP:** при partition сеть — выбор CP vs AP (PostgreSQL sync rep → CP bias).

**Read replicas:** отчёты на standby, снижение нагрузки на primary (OLAP на replica).""",
    [("morgunov", "Глава 22, §22.2"), ("novikov", "Глава 16, §16.1")],
    [("Streaming replication", "физическая WAL-репликация"), ("Logical replication", "табличная публикация"),
     ("Standby", "реplica-сервер"), ("Failover", "переключение primary")]),
"quiz": quiz("p7-l06-replication",
    sq("q1", "Streaming replication передаёт…", ["WAL поток", "Only SQL queries", "MongoDB oplog", "CSV"], 0, "Physical WAL stream."),
    sq("q2", "Logical replication…", ["Выборочные таблицы", "Full cluster byte copy only", "No WAL", "Only backup"], 0, "Table-level pub/sub."),
    sq("q3", "hot_standby позволяет…", ["SELECT на replica", "Write on standby", "No connection", "Drop primary"], 0, "Read-only queries."),
    sq("q4", "Synchronous replication улучшает…", ["Durability (RPO)", "Write speed always", "No lag ever guaranteed", "MongoDB"], 0, "Commit waits for standby."),
    mq("q5", "Failover planning? (верные)", ["Monitoring lag", "Promotion procedure", "Split-brain prevention", "Ignore WAL"], [0,1,2], "HA planning.")),
"tasks": """## Задания

1. Опишите архитектуру primary + 1 standby.
2. Logical vs streaming — когда что?
3. Что такое replication lag и как мониторить?
4. Связь replication и CAP (partition tolerance).""",
}

LESSONS["p7-l07-oltp-olap"] = {
"md": md("OLTP vs OLAP: сравнение нагрузок", P7, M7, TH,
    ["Различить транзакционную и аналитическую нагрузку", "Сопоставить нормализацию и денormalization", "Выбрать архитектуру под сценарий"],
    """**OLTP:** много коротких транзакций (INSERT оценки, UPDATE профиля). 3NF, индексы на PK/FK, row-level locks, low latency.

**OLAP:** тяжёлые read, агрегаты, scan больших объёмов. Star schema, denormalized dimensions, columnar (ClickHouse, etc.), batch load.

| | OLTP | OLAP |
|---|------|------|
| Запросы | Короткие точечные | Scan + GROUP BY |
| Схема | Нормализованная | Star/snowflake |
| Consistency | Strong ACID | Often eventual in loads |
| Пример | university OLTP | DWH успеваемости |

**CAP (Brewer):** в partition — выбор **C** (consistency) vs **A** (availability). PostgreSQL sync rep → CP; async → AP bias с lag.

**HTAP:** гибриды (PostgreSQL + columnar extension) — компромисс.

Архитектура: OLTP → ETL/CDC → DWH для отчётов; не гонять OLAP на primary без replica.""",
    [("lecture1", "Слайды 80–95"), ("smirnov", "Глава 1: OLTP и OLAP")],
    [("OLTP", "транзакционная нагрузка"), ("OLAP", "аналитическая нагрузка"),
     ("CAP", "consistency/availability/partition"), ("Denormalization", "для аналитики")]),
"quiz": quiz("p7-l07-oltp-olap",
    sq("q1", "OLTP характеризуется…", ["Много коротких транзакций", "Только batch scan", "No indexes", "Only CSV"], 0, "Transactional workload."),
    sq("q2", "OLAP часто использует…", ["Star schema", "3NF only", "No aggregation", "MongoDB only"], 0, "Dimensional model."),
    sq("q3", "CAP: при partition сеть…", ["Trade-off C vs A", "Both always", "Neither", "WAL off"], 0, "Partition tolerance forces choice."),
    sq("q4", "OLAP на primary OLTP…", ["Плохая идея без replica", "Always best", "Required", "Replaces backup"], 0, "Separate workloads."),
    mq("q5", "OLTP design? (верные)", ["Normalization", "Indexes on FK", "Short transactions", "Full table scan reports"], [0,1,2], "OLTP patterns.")),
"tasks": """## Задания

1. Классифицируйте: «вставить оценку» vs «средний балл по факультетам за 5 лет».
2. Нарисуйте OLTP → ETL → DWH для университета.
3. Объясните CAP на примере async replication.
4. Когда star schema вместо 3NF?""",
}

LESSONS["p7-l08-exam"] = {
"md": md("Контроль: безопасность, резервирование и OLTP/OLAP", P7, M7, EX,
    ["Спроектировать модель доступа", "Выполнить backup/restore", "Обосновать выбор OLTP или OLAP"],
    """Итог части 7: pg_hba/auth, GRANT/REVOKE, RLS, encryption, pg_dump/basebackup, replication, OLTP/OLAP/CAP.

Комплексный сценарий: учебная БД университета — роли (student/teacher/admin), RLS на performance, backup policy, read replica для отчётов.""",
    [("morgunov", "Главы 21–22 (повторение)"), ("novikov", "Главы 15–16 (повторение)")],
    [("GRANT", "авторизация"), ("RLS", "строки"), ("Backup", "pg_dump/PITR"), ("Replication", "HA/read scale")]),
"quiz": quiz("p7-l08-exam",
    sq("q1", "Студент видит только свои строки…", ["RLS policy", "CROSS JOIN", "TOAST", "BRIN only"], 0, "Row security."),
    sq("q2", "pg_dump vs basebackup…", ["Logical vs physical", "Same thing", "Only Mongo", "Only WAL"], 0, "Backup types."),
    sq("q3", "Least privilege…", ["Минимум прав", "ALL to PUBLIC", "trust all", "No roles"], 0, "Security."),
    sq("q4", "Async replication CAP…", ["AP with lag", "Always CP", "No partition", "No WAL"], 0, "Availability bias."),
    mq("q5", "Часть 7 topics? (верные)", ["Security", "Backup", "Replication OLTP/OLAP", "Graph Cypher only"], [0,1,2], "Admin topics.")),
"tasks": """## Итоговая работа

1. Модель ролей: admin, teacher, student для university DB.
2. RLS: student → только свои performance.
3. pg_dump + restore test.
4. Схема primary + replica для отчётов.
5. Эссе: OLTP vs OLAP для деканата.""",
}

# ===== PART 8 =====
LESSONS["p8-l01-dwh-concepts"] = {
"md": md("Хранилища данных: понятия и архитектура", P8, M8, TH,
    ["Определить DWH, Data Mart и Data Lake", "Описать слои staging и core", "Сопоставить Inmon и Kimball"],
    """**DWH (Data Warehouse)** — предметно-ориентированное, интегрированное, неvolatile, time-variant хранилище для аналитики (Inmon).

**Data Mart** — витрина под департамент (продажи, успеваемость).

**Data Lake** — сырьё (raw files) в object storage; schema-on-read.

**Слои:**
- **Staging** — сырые копии из источников (OLTP).
- **Core/Integration** — очистка, conform dimensions (Inmon bus architecture).
- **Presentation** — star schemas, marts, reports.

**Inmon:** сверху-вниз, normalized enterprise DWH → marts.
**Kimball:** снизу-вверх, dimensional star schemas по процессам (факты + измерения).

Для **университета:** источник — OLTP (student, performance); DWH — история успеваемости, агрегаты по группам/кафедрам.""",
    [("smirnov", "Глава 1–2"), ("lecture1", "Слайды 96–110")],
    [("DWH", "аналитическое хранилище"), ("Staging", "промежуточная зона"),
     ("Inmon", "корпоративное DWH"), ("Kimball", "dimensional modeling")]),
"quiz": quiz("p8-l01-dwh-concepts",
    sq("q1", "DWH отличается от OLTP…", ["Ориентация на аналитику", "Только INSERT", "No history", "3NF forbidden"], 0, "Analytical focus."),
    sq("q2", "Kimball фокус…", ["Star schemas / dimensions", "Only 6NF", "MongoDB", "No facts"], 0, "Dimensional."),
    sq("q3", "Staging layer…", ["Сырые данные из источников", "Final reports", "OLTP transactions", "WAL"], 0, "Landing zone."),
    sq("q4", "Data Mart…", ["Subject-area subset", "Full lake only", "Replacing OLTP", "pg_hba"], 0, "Department mart."),
    mq("q5", "DWH properties? (верные)", ["Integrated", "Time-variant", "Non-volatile", "Real-time OLTP only"], [0,1,2], "Inmon criteria.")),
"tasks": """## Задания

1. Сравните Inmon и Kimball (таблица 5 строк).
2. Нарисуйте слои: OLTP → staging → core → mart для университета.
3. Data Lake vs DWH — когда lake?
4. Прочитайте Smirnov гл. 1–2.""",
}

LESSONS["p8-l02-dimensional"] = {
"md": md("Измерения и факты: основы dimensional modeling", P8, M8, TH,
    ["Выделить fact и dimension таблицы", "Определить grain фактовой таблицы", "Спроектировать surrogate key"],
    """**Fact table** — метрики (measures): оценка, сумма продаж, количество. **Grain** — что означает одна строка («одна оценка студента за экзамен»).

**Dimension** — контекст: студент, время, дисциплина, группа. Denormalized атрибуты для удобства фильтрации.

**Surrogate key** — искусственный PK dimension (student_key), отдельно от business key (student_id из OLTP).

**Types of facts:** additive (sum), semi-additive (balance), non-additive (ratio).

Пример университета:
- Fact: `fact_performance` (student_key, date_key, subject_key, grade)
- Dim: `dim_student`, `dim_date`, `dim_subject`

**Slowly Changing Dimensions (SCD):** Type 1 overwrite; Type 2 history rows with effective dates.""",
    [("smirnov", "Глава 3"), ("info-support", "Раздел 5: измерения")],
    [("Fact", "таблица метрик"), ("Dimension", "контекст анализа"),
     ("Grain", "детализация строки факта"), ("Surrogate key", "суррогатный ключ")]),
"quiz": quiz("p8-l02-dimensional",
    sq("q1", "Grain факта — это…", ["Что описывает одна строка", "PK dimension", "WAL size", "Index type"], 0, "Fact granularity."),
    sq("q2", "Surrogate key…", ["Искусственный PK dimension", "Business natural key only", "WAL LSN", "Mongo _id only"], 0, "Warehouse PK."),
    sq("q3", "Оценка в fact table — …", ["Measure", "Dimension", "Staging", "pg_hba"], 0, "Numeric measure."),
    sq("q4", "SCD Type 2…", ["История изменений dimension", "Overwrite", "Delete all", "No dates"], 0, "Historical tracking."),
    mq("q5", "Dimension содержит… (верные)", ["Descriptive attributes", "Filters for reports", "Surrogate key", "Only WAL"], [0,1,2], "Dimension role.")),
"tasks": """## Задания

1. Для fact «продажи» определите grain.
2. dim_student: какие атributы (имя, группа, факультет)?
3. SCD: студент перевёлся в другую группу — Type 1 vs 2?
4. Surrogate vs natural key — зачем surrogate?""",
}

LESSONS["p8-l03-star-schema"] = {
"md": md("Звезда (Star Schema)", P8, M8, TH,
    ["Построить star schema для продаж", "Денormalize измерения", "Оценить производительность запросов"],
    """**Star schema:** центральная **fact** + **dimensions** вокруг (радиальная схема). Dimensions **denormalized** (все атрибуты группы в dim_student).

```
        dim_date
            |
dim_student — fact_performance — dim_subject
            |
        dim_group
```

**Плюсы:** простые JOIN, быстрые агрегаты для BI, понятно бизнесу.
**Минусы:** redundancy в dimensions, риск inconsistency без ETL discipline.

**Запрос:** средний балл по факультетам за семестр — JOIN fact + dim_student + dim_date, GROUP BY faculty.

**Университет (design task):** grain = одна оценка; facts: grade, attempt; dims: student (name, group_id, faculty), date (semester, year), subject (name, department).""",
    [("smirnov", "Глава 4, §4.1"), ("practicum", "Глава 8: star schema")],
    [("Star schema", "fact + denormalized dims"), ("Fact table", "центр звезды"),
     ("Denormalization", "для скорости чтения")],
    extra="\nСквозная предметная область: **университет** — звезда для успеваемости.\n"),
"quiz": quiz("p8-l03-star-schema",
    sq("q1", "Star schema имеет…", ["Одну fact и несколько dimensions", "Только 3NF", "No facts", "Graph edges"], 0, "Star pattern."),
    sq("q2", "Dimensions в star…", ["Denormalized", "Always 5NF", "No attributes", "Only PK"], 0, "Wide dimensions."),
    sq("q3", "Fact_performance grain…", ["Одна оценка за экзамен", "Весь студент", "Вся группа", "WAL record"], 0, "Fine-grained fact."),
    sq("q4", "Star vs OLTP 3NF…", ["Star for read analytics", "Star for OLTP writes", "Identical", "No JOINs in star"], 0, "Analytical optimization."),
    mq("q5", "Star query pattern? (верные)", ["JOIN fact to dims", "GROUP BY dim attrs", "Filter on dimensions", "Only CROSS JOIN"], [0,1,2], "Typical BI query.")),
"tasks": """## Задания — проектирование star schema университета

**Обязательное задание:** спроектируйте star schema для аналитики успеваемости.

1. **Fact table** `fact_grade` — определите grain и measures (grade, credits, is_pass).
2. **Dimensions:** `dim_student`, `dim_group`, `dim_subject`, `dim_date`, `dim_department`.
3. Для каждой dimension перечислите 5+ атрибутов (denormalized где нужно).
4. Нарисуйте диаграмму звезды (draw.io).
5. Напишите SQL-запрос: средний балл по кафедрам за 2024–2025 уч. год.
6. Обоснуйте выбор grain и surrogate keys.""",
}

LESSONS["p8-l04-snowflake"] = {
"md": md("Снежинка (Snowflake Schema)", P8, M8, TH,
    ["Нормализовать измерения в snowflake", "Сравнить star и snowflake", "Выбрать схему для ETL"],
    """**Snowflake** — dimensions **нормализованы** в иерархии:

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

Kimball: обычно star; snowflake — когда dimensions очень большие или shared conformed dimensions (Inmon bus).""",
    [("smirnov", "Глава 4, §4.2"), ("komarov", "Раздел 15: snowflake")],
    [("Snowflake schema", "нормализованные dimensions"), ("Conformed dimension", "общее измерение"),
     ("Hierarchy", "faculty → university")]),
"quiz": quiz("p8-l04-snowflake",
    sq("q1", "Snowflake отличается…", ["Нормализованные dimensions", "No fact table", "Only MongoDB", "WAL"], 0, "Normalized dims."),
    sq("q2", "Star проще для…", ["BI users и queries", "Only ETL", "Write OLTP", "Backup"], 0, "Fewer joins."),
    sq("q3", "Snowflake снижает…", ["Redundancy in dims", "All JOINs", "Need for facts", "Storage always zero"], 0, "Normalized storage."),
    sq("q4", "Conformed dimension…", ["Одинаковое измерение в marts", "Unique to one fact", "OLTP only", "pg_trgm"], 0, "Shared dim."),
    mq("q5", "Choose snowflake when? (верные)", ["Large shared hierarchies", "Storage cost matters", "Strict conformity", "Always over star"], [0,1,2], "Trade-offs.")),
"tasks": """## Задания

1. Перерисуйте star universiteta v snowflake (faculty отдельно).
2. Сосчитайте JOIN для «средний балл по faculty» в star vs snowflake.
3. Когда выбрали бы star для деканата?
4. Smirnov §4.2.""",
}

LESSONS["p8-l05-etl"] = {
"md": md("ETL и ELT: загрузка данных в DWH", P8, M8, TH,
    ["Описать этапы extract, transform, load", "Сравнить ETL и ELT", "Спроектировать staging area"],
    """**ETL:** Extract (OLTP, APIs) → Transform (cleanse, conform, surrogate keys) → Load (fact/dim).

**ELT:** Extract → Load raw to staging (cloud DWH) → Transform in SQL (BigQuery, Snowflake).

**Staging area:** копии source tables; validation; audit columns (load_date, batch_id).

**Steps для university DWH:**
1. Extract student, performance из PostgreSQL OLTP.
2. Transform: lookup surrogate keys, handle SCD Type 2 для student.
3. Load fact_grade, refresh dim_*.

**Quality:** dedup, null checks, FK integrity, reconciliation counts.

**Tools:** pg_dump/COPY, Apache Airflow, dbt, custom Python/SQL scripts.

Smirnov: медленно меняющиеся измерения, late arriving facts, incremental load.""",
    [("smirnov", "Глава 5"), ("lecture1", "Слайды 111–120")],
    [("ETL", "extract-transform-load"), ("Staging", "промежуточная область"),
     ("Incremental load", "дельта-загрузка"), ("dbt", "transform in warehouse")]),
"quiz": quiz("p8-l05-etl",
    sq("q1", "Extract в ETL…", ["Читает источники", "Only BI", "Drop DWH", "VACUUM"], 0, "Source read."),
    sq("q2", "ELT transform…", ["В хранилище после load", "Before extract", "Never", "Only Mongo"], 0, "Transform in DWH."),
    sq("q3", "Staging для…", ["Валидации и audit", "Final reports only", "OLTP writes", "RLS"], 0, "Landing/QA."),
    sq("q4", "Surrogate keys назначаются…", ["В transform", "In OLTP only", "Never", "pg_hba"], 0, "DW transform step."),
    mq("q5", "ETL quality checks? (верные)", ["Row counts", "Null keys", "Duplicate detection", "Ignore all"], [0,1,2], "Data quality.")),
"tasks": """## Задания

1. Опишите ETL pipeline OLTP performance → fact_grade (5 шагов).
2. Incremental vs full load — когда что?
3. SCD Type 2 при ETL смены группы студента.
4. Reconciliation: count OLTP vs fact.""",
}

LESSONS["p8-l06-olap-cubes"] = {
"md": md("OLAP-кубы и операции drill-down", P8, M8, TH,
    ["Выполнить slice, dice, roll-up", "Объяснить ROLAP vs MOLAP", "Построить простой OLAP-отчёт"],
    """**OLAP operations:**
- **Slice** — фиксируем одно измерение (semester=1).
- **Dice** — подcube по нескольким фильтрам.
- **Roll-up** — агрегация вверх (день → месяц → год).
- **Drill-down** — детализация (faculty → group → student).

**ROLAP:** SQL over star schema (PostgreSQL, ClickHouse).
**MOLAP:** precomputed cube (SSAS, Essbase) — быстрый, less flexible.
**HOLAP:** hybrid.

SQL roll-up:
```sql
SELECT d.year, d.semester, avg(f.grade)
FROM fact_grade f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY ROLLUP (d.year, d.semester);
```

Smirnov: куб = метрика по осям dimensions; pivot tables в Excel — простой OLAP UI.""",
    [("smirnov", "Глава 6"), ("novikov", "Глава 17, §17.2")],
    [("Slice/Dice", "выбор подмножества куба"), ("Roll-up", "агрегация"),
     ("ROLAP", "SQL-based OLAP"), ("MOLAP", "multidimensional storage")]),
"quiz": quiz("p8-l06-olap-cubes",
    sq("q1", "Roll-up…", ["Агрегирует к более coarse grain", "Details only", "DELETE facts", "WAL"], 0, "Aggregation up."),
    sq("q2", "Drill-down…", ["Детализация", "Delete dim", "Backup", "RLS"], 0, "More detail."),
    sq("q3", "ROLAP использует…", ["Relational star schema", "Only binary cube", "MongoDB only", "No SQL"], 0, "SQL OLAP."),
    sq("q4", "GROUP BY ROLLUP…", ["Иерархические subtotals", "Only one row", "CROSS JOIN", "TOAST"], 0, "SQL rollup."),
    mq("q5", "OLAP ops? (верные)", ["Slice", "Dice", "Pivot", "VACUUM"], [0,1,2], "Classic ops.")),
"tasks": """## Задания

1. Slice: только spring semester — SQL filter.
2. Roll-up: оценки year → semester → month (если есть date dim).
3. ROLAP vs MOLAP для университета?
4. Smirnov гл. 6.""",
}

LESSONS["p8-l07-data-marts"] = {
"md": md("Витрины данных (Data Marts)", P8, M8, TH,
    ["Спроектировать subject-area mart", "Определить SLA обновления", "Интегрировать mart с DWH"],
    """**Data Mart** — subset DWH для одной предметной области (деанат, admissions, finance).

**Dependent mart** — из enterprise DWH (Inmon).
**Independent mart** — Kimball standalone star для быстрого старта.

**SLA:** nightly batch vs hourly incremental; freshness vs cost.

**University marts:**
- **Mart успеваемости** — fact_grade + dims; users: деканат.
- **Mart контингента** — dim_student snapshots; users: учебный отдел.

**Integration:** conformed dimensions (dim_date, dim_student) across marts для cross-reporting.

**Security:** mart-level GRANT; row filters по faculty (аналог RLS в presentation layer).""",
    [("smirnov", "Глава 7"), ("info-support", "Раздел 6: витрины")],
    [("Data Mart", "предметная витрина"), ("SLA", "соглашение о свежести"),
     ("Conformed dimension", "сквозное измерение")]),
"quiz": quiz("p8-l07-data-marts",
    sq("q1", "Data Mart…", ["Subject-area analytics", "OLTP system", "WAL archive", "Mongo only"], 0, "Department focus."),
    sq("q2", "Conformed dim…", ["Shared across marts", "Unique name only", "No surrogate", "Staging only"], 0, "Enterprise consistency."),
    sq("q3", "SLA defines…", ["Refresh frequency/latency", "SQL dialect", "Index type", "TOAST"], 0, "Service level."),
    sq("q4", "Dependent mart sources…", ["Enterprise DWH", "Only Excel", "Never ETL", "pg_hba"], 0, "Top-down Inmon."),
    mq("q5", "Mart design? (верные)", ["Clear users", "Defined grain", "Refresh policy", "No facts"], [0,1,2], "Mart checklist.")),
"tasks": """## Задания

1. Опишите mart для деканата факультета IT (tables, users, SLA nightly).
2. Какие conformed dimensions с mart контингента?
3. Independent vs dependent mart — пример.
4. Smirnov гл. 7.""",
}

LESSONS["p8-l08-dwh-lab"] = {
"md": md("Кейс: проектирование хранилища продаж", P8, M8, LAB,
    ["Построить star schema для retail", "Написать ETL-скрипт загрузки", "Сформировать аналитический отчёт"],
    """**Лабораторная:** retail sales DWH (Smirnov практика) + параллельно **university star** из p8-l03.

**Retail star:**
- fact_sales (sale_id grain): quantity, amount, discount
- dim_product, dim_customer, dim_store, dim_date

**ETL sketch (PostgreSQL staging):**
```sql
CREATE TABLE stg_sales AS SELECT * FROM oltp.sales WHERE sale_date >= current_date - 1;
INSERT INTO fact_sales SELECT ... surrogate lookups ... FROM stg_sales;
```

**Отчёт:** выручка по магазинам и категориям за месяц.

**University extension:** fact_grade + dims; отчёт — топ-5 групп по среднему баллу.""",
    [("smirnov", "Глава 8 (практика)"), ("practicum", "Задание 8: DWH")],
    [("Retail star", "fact_sales"), ("ETL script", "staging to fact"), ("BI report", "GROUP BY aggregates")]),
"quiz": quiz("p8-l08-dwh-lab",
    sq("q1", "fact_sales grain…", ["Одна строка продажи", "Весь магазин", "One day all sales", "Student"], 0, "Line item sale."),
    sq("q2", "Staging перед load…", ["Validate source data", "Replace OLTP", "Skip transform", "WAL only"], 0, "QA layer."),
    sq("q3", "Surrogate lookup в ETL…", ["JOIN dim by business key", "Random UUID only", "No dims", "CROSS JOIN"], 0, "Key mapping."),
    sq("q4", "Отчёт retail…", ["SUM(amount) BY store", "Only INSERT", "VACUUM", "RLS"], 0, "Aggregate report."),
    mq("q5", "Lab deliverables? (верные)", ["Star diagram", "ETL SQL", "Analytical query", "Mongo install"], [0,1,2], "Lab outputs.")),
"tasks": """## Лабораторная

**Retail (Smirnov):**
1. Star schema: fact_sales + 4 dimensions (diagram).
2. DDL PostgreSQL для fact и dims.
3. ETL: stg → fact (INSERT script).
4. Отчёт: revenue by store, month.

**University (дополнительно):**
5. Star schema успеваемости (из p8-l03).
6. SQL: top-5 групп по avg(grade).

Сохраните: `course/sql/p8-l08-dwh-lab.sql`""",
}

LESSONS["p8-l09-exam"] = {
"md": md("Контроль: проектирование хранилищ данных", P8, M8, EX,
    ["Спроектировать dimensional model", "Обосновать выбор star/snowflake", "Описать pipeline загрузки данных"],
    """Итог части 8: Inmon/Kimball, facts/dimensions/grain, star/snowflake, ETL/ELT, OLAP ops, marts.

**Экзаменационный кейс:** университет — построить DWH успеваемости: star schema, ETL из OLTP, OLAP запрос (roll-up по faculty), SLA mart для деканата.""",
    [("smirnov", "Главы 1–8 (повторение)"), ("lecture1", "Слайды 96–120 (повторение)")],
    [("Dimensional model", "facts+dims"), ("Star", "denormalized"), ("ETL", "pipeline"), ("OLAP", "slice/roll-up")]),
"quiz": quiz("p8-l09-exam",
    sq("q1", "Kimball акцент…", ["Dimensional stars", "Only 6NF OLTP", "Mongo only", "No ETL"], 0, "Kimball method."),
    sq("q2", "Grain определяет…", ["Строку fact", "WAL", "Index", "Role"], 0, "Fact row meaning."),
    sq("q3", "Star для university grades…", ["fact_grade + dims", "Only OLTP 3NF", "Graph DB", "pg_hba"], 0, "Analytical schema."),
    sq("q4", "Roll-up in SQL…", ["GROUP BY coarser dim", "DELETE", "TRUNCATE staging", "RLS off"], 0, "Aggregation."),
    mq("q5", "Part 8 topics? (верные)", ["Inmon/Kimball", "ETL", "Star schema", "PostgreSQL WAL only"], [0,1,2], "DWH topics.")),
"tasks": """## Итоговая работа

1. Полный dimensional design university DWH (diagram + DDL).
2. Star vs snowflake — обоснование.
3. ETL pipeline (10 шагов).
4. 3 OLAP запроса: slice, roll-up, drill-down.
5. Все тесты части 8 ≥70%.""",
}

# ===== PART 9 =====
LESSONS["p9-l01-nosql-overview"] = {
"md": md("NoSQL: обзор моделей и сценариев", P9, M9A, TH,
    ["Классифицировать document, key-value, graph, column", "Сопоставить NoSQL и реляционные БД", "Выбрать технологию под use case"],
    """**NoSQL** — не «no SQL», а «not only SQL»; отказ от строгой relational модели ради scale/flexibility.

| Модель | Пример | Use case |
|--------|--------|----------|
| Document | MongoDB | JSON catalog, CMS |
| Key-value | Redis | Cache, sessions |
| Column-family | Cassandra | Time series, wide rows |
| Graph | Neo4j | Social, fraud, paths |

**vs RDBMS:** схема гибкая vs rigid; horizontal scale vs vertical; eventual consistency vs ACID (часто); JOIN expensive vs normalized.

**Когда PostgreSQL достаточно:** JSONB + GIN, pgvector, ltree — «SQL + extensions».

**Когда MongoDB:** nested documents, rapid schema change, shard by access pattern.

**Когда Graph:** many-hop relationships (friends-of-friends), shortest path — JOIN hell в SQL.""",
    [("mongodb", "Глава 1"), ("graph-db", "Глава 1")],
    [("Document DB", "JSON/BSON documents"), ("Key-value", "K-V store"),
     ("Graph DB", "vertices and edges"), ("CAP", "trade-offs at scale")]),
"quiz": quiz("p9-l01-nosql-overview",
    sq("q1", "Document DB хранит…", ["JSON/BSON documents", "Only tables 3NF", "WAL only", "pg_hba"], 0, "Document model."),
    sq("q2", "Graph DB силён в…", ["Path traversal", "Simple ledger OLTP only", "Only backup", "FTS"], 0, "Relationship queries."),
    sq("q3", "Redis — …", ["Key-value store", "Relational", "Column DWH", "WAL"], 0, "In-memory KV."),
    sq("q4", "PostgreSQL JSONB…", ["Hybrid document in SQL", "Replaces Mongo always", "No indexes", "Graph native"], 0, "JSON in RDBMS."),
    mq("q5", "NoSQL fit? (верные)", ["Flexible schema", "Horizontal scale", "Specific access patterns", "Always replace PG"], [0,1,2], "Selective use.")),
"tasks": """## Задания

1. Классифицируйте: каталог товаров, кэш сессий, social network, OLTP банк.
2. Когда university OLTP остаётся в PostgreSQL?
3. Сравните CAP для Cassandra vs PostgreSQL sync rep.
4. MongoDB + Graph DB гл. 1.""",
}

LESSONS["p9-l02-mongo-model"] = {
"md": md("MongoDB: документная модель и BSON", P9, M9A, TH,
    ["Описать коллекции и документы", "Спроектировать вложенную схему", "Сравнить embedding и referencing"],
    """**MongoDB:** database → **collection** → **document** (BSON). Нет фиксированной схемы (flexible schema).

```json
{
  "_id": ObjectId("..."),
  "student_id": 101,
  "name": "Иванов",
  "group": { "code": "ИВТ-21", "faculty": "IT" },
  "grades": [ { "subject": "БД", "score": 5 } ]
}
```

**Embedding** — вложенные массивы/объекты: один read, atomic update документа; но document size limit 16MB, duplication.

**Referencing** — `$lookup` или manual refs like SQL FK: normalization, smaller docs; нужны доп. queries.

**vs PostgreSQL JSONB:** Mongo — native sharding, aggregation pipeline; PG — ACID, JOIN, один стек.

""" + OPT,
    [("mongodb", "Главы 2–3"), ("komarov", "Раздел 16: document DB")],
    [("Collection", "набор документов"), ("BSON", "binary JSON"),
     ("Embedding", "вложение данных"), ("Referencing", "ссылки между docs")]),
"quiz": quiz("p9-l02-mongo-model",
    sq("q1", "MongoDB document…", ["BSON record in collection", "SQL table row only", "WAL segment", "Index only"], 0, "Document unit."),
    sq("q2", "Embedding подходит…", ["One-to-few nested data", "Unlimited 100MB arrays", "Cross-shard JOIN", "Graph paths"], 0, "Bounded nesting."),
    sq("q3", "_id в MongoDB…", ["Primary key document", "Foreign key only", "WAL LSN", "Schema name"], 0, "Default PK."),
    sq("q4", "Referencing vs embedding…", ["Normalize vs denormalize trade-off", "Same always", "No choice", "PG only"], 0, "Modeling choice."),
    mq("q5", "Mongo design? (верные)", ["Access pattern first", "16MB doc limit", "Shard key matters", "Always 3NF"], [0,1,2], "Document modeling.")),
"tasks": """## Задания (опционально — без установки MongoDB)

""" + OPT + """
1. Спроектируйте document для student+grades: embedding vs referencing — 2 варианта JSON.
2. Когда embedding grades в student doc?
3. Эквивалент PostgreSQL: JSONB column vs normalized tables.
4. MongoDB Playground: создайте sample document (опционально).""",
}

LESSONS["p9-l03-mongo-queries"] = {
"md": md("MongoDB: CRUD и запросы", P9, M9A, TH,
    ["Выполнить find, insert, update, delete", "Использовать операторы $gt, $in, $regex", "Создать индексы в MongoDB"],
    """**CRUD (MongoDB shell / driver):**

```javascript
db.students.insertOne({ name: "Петров", group: "ИВТ-21" })
db.students.find({ "grades.score": { $gt: 4 } })
db.students.updateOne({ name: "Петров" }, { $set: { status: "active" } })
db.students.deleteMany({ status: "inactive" })
```

**Operators:** `$gt`, `$gte`, `$in`, `$regex`, `$elemMatch`.

**Indexes:** `db.students.createIndex({ group: 1, name: 1 })`

**PostgreSQL equivalent:**

| Mongo | PostgreSQL |
|-------|------------|
| find({a:1}) | SELECT * WHERE a=1 |
| $gt | > |
| $in | IN (...) |
| insertOne | INSERT ... RETURNING |
| updateOne $set | UPDATE ... SET |

""" + OPT,
    [("mongodb", "Главы 4–5"), ("practicum", "Задание 9: MongoDB")],
    [("find", "query documents"), ("$operators", "filter operators"), ("createIndex", "index in Mongo")]),
"quiz": quiz("p9-l03-mongo-queries",
    sq("q1", "find({score: {$gt: 4}})…", ["score > 4", "score = 4", "score < 4", "DELETE"], 0, "$gt greater than."),
    sq("q2", "$in в Mongo…", ["Match any in list", "Index only", "JOIN", "WAL"], 0, "IN equivalent."),
    sq("q3", "updateOne…", ["Updates first match", "All documents always", "Drop collection", "CREATE TABLE"], 0, "Single doc update."),
    sq("q4", "PG equivalent find filter…", ["WHERE clause", "GROUP BY", "VACUUM", "GRANT"], 0, "SQL WHERE."),
    mq("q5", "Mongo CRUD? (верные)", ["insertOne", "find", "updateOne", "MERGE native"], [0,1,2], "Basic ops.")),
"tasks": """## Задания (опционально)

""" + OPT + """
1. Запишите find для students с grade > 4 в группе ИВТ-21.
2. PG equivalent: SELECT с WHERE и JOIN.
3. Какие индексы для { group: 1, "grades.score": 1 }?
4. Playground: выполните insert + find (опционально).""",
}

LESSONS["p9-l04-mongo-aggregation"] = {
"md": md("MongoDB: aggregation pipeline", P9, M9A, TH,
    ["Построить pipeline $match, $group, $lookup", "Сформировать аналитический отчёт", "Сравнить с SQL GROUP BY"],
    """**Aggregation pipeline** — stages left-to-right:

```javascript
db.performance.aggregate([
  { $match: { year: 2025 } },
  { $group: { _id: "$group", avgGrade: { $avg: "$grade" } } },
  { $sort: { avgGrade: -1 } },
  { $lookup: { from: "groups", localField: "_id", foreignField: "code", as: "g" } }
])
```

**Stages:** $match (filter), $group (aggregate), $project, $lookup (left join), $unwind (flatten array).

**SQL equivalent:**
```sql
SELECT group_id, avg(grade) FROM performance WHERE year=2025 GROUP BY group_id ORDER BY 2 DESC;
-- $lookup ≈ LEFT JOIN
```

Для DWH-grade analytics часто проще SQL/star schema; Mongo aggregation — когда data already in documents.

""" + OPT,
    [("mongodb", "Глава 6"), ("headfirst", "Приложение: NoSQL")],
    [("$match", "filter stage"), ("$group", "aggregation"), ("$lookup", "join-like stage")]),
"quiz": quiz("p9-l04-mongo-aggregation",
    sq("q1", "$group похож на…", ["SQL GROUP BY", "CREATE INDEX", "VACUUM", "RLS"], 0, "Aggregation."),
    sq("q2", "$lookup…", ["Join-like between collections", "Delete", "Insert only", "WAL"], 0, "Left outer join."),
    sq("q3", "$match первым для…", ["Reduce documents early", "Slow query", "No reason", "Backup"], 0, "Filter early."),
    sq("q4", "$avg в $group…", ["Average measure", "Primary key", "Index type", "Shard key"], 0, "Aggregator."),
    mq("q5", "Pipeline stages? (верные)", ["$match", "$group", "$lookup", "$CHECKPOINT"], [0,1,2], "Common stages.")),
"tasks": """## Задания (опционально)

""" + OPT + """
1. Pipeline: avg grade by group, top 5.
2. SQL equivalent с GROUP BY и ORDER BY.
3. Когда star schema лучше aggregation Mongo?
4. Playground pipeline (опционально).""",
}

LESSONS["p9-l05-graph-intro"] = {
"md": md("Графовые базы данных: модель и применение", P9, M9A, TH,
    ["Определить вершины, рёбра и свойства", "Привести примеры social и fraud graphs", "Оценить преимущества перед RDBMS"],
    """**Property Graph:** **vertices (nodes)** + **edges (relationships)** + properties on both.

Примеры:
- **Social:** Person —FRIEND→ Person; recommendation, communities.
- **Fraud:** Account —TRANSFER→ Account; cycle detection, mule networks.
- **University:** Student —ENROLLED→ Course —TAUGHT_BY→ Teacher; prerequisites chain.

**vs RDBMS:** recursive CTE в SQL для graphs возможен, но multi-hop (6+) дорог (JOIN explosion). Graph DB: **index-free adjacency**, native traversal O(edges) not O(rows).

**Neo4j, Amazon Neptune, etc.** — Cypher, Gremlin query languages.

**When not graph:** simple FK relationships, reporting aggregates — PostgreSQL достаточно.""",
    [("graph-db", "Главы 2–3"), ("komarov", "Раздел 17: graph DB")],
    [("Vertex", "узел графа"), ("Edge", "relationship"), ("Traversal", "обход графа"),
     ("Index-free adjacency", "быстрый local hop")]),
"quiz": quiz("p9-l05-graph-intro",
    sq("q1", "Graph DB vertex…", ["Node/entity", "SQL table only", "WAL", "Index B-tree only"], 0, "Node."),
    sq("q2", "Edge represents…", ["Relationship", "Primary key", "Backup", "Schema"], 0, "Relationship."),
    sq("q3", "Multi-hop friends…", ["Graph traversal", "CROSS JOIN only", "TRUNCATE", "TOAST"], 0, "Path query."),
    sq("q4", "Fraud ring detection…", ["Graph pattern match", "Only COUNT(*)", "VACUUM", "pg_dump"], 0, "Pattern in graph."),
    mq("q5", "Graph fit? (верные)", ["Social networks", "Path finding", "Network topology", "Simple ledger 2 tables"], [0,1,2], "Graph use cases.")),
"tasks": """## Задания

1. Нарисуйте graph: Student-Course-Teacher для университета.
2. SQL recursive CTE vs graph — 3-hop friends, что проще?
3. Fraud: найти cycle transfers — почему graph?
4. Graph DB гл. 2–3.""",
}

LESSONS["p9-l06-graph-queries"] = {
"md": md("Graph DB: Cypher и обход графа", P9, M9A, TH,
    ["Написать MATCH и RETURN в Cypher", "Выполнить k-hop обход", "Сравнить производительность с JOIN"],
    """**Cypher (Neo4j):**

```cypher
MATCH (s:Student {name: 'Иванов'})-[:ENROLLED]->(c:Course)
RETURN c.name, c.credits

MATCH (a:Person)-[:FRIEND*1..3]-(b:Person)
WHERE a.name = 'Alice'
RETURN DISTINCT b.name

MATCH path = (s:Student)-[:PREREQ*]->(c:Course {name: 'БД'})
RETURN path
```

**k-hop:** variable length `[*1..k]` — друзья до 3 уровня.

**vs SQL:**
```sql
WITH RECURSIVE hops AS (
  SELECT friend_id, 1 AS depth FROM friends WHERE user_id = 1
  UNION ALL
  SELECT f.friend_id, h.depth+1 FROM friends f JOIN hops h ON f.user_id = h.friend_id WHERE h.depth < 3
) SELECT * FROM hops;
```

Graph wins on deep/varied traversals; SQL wins on aggregates over star schema.

Опционально: [Neo4j Browser sandbox](https://sandbox.neo4j.com) без локальной установки.""",
    [("graph-db", "Главы 4–5"), ("mongodb", "Глава 7 (сравнение)")],
    [("Cypher", "язык запросов Neo4j"), ("MATCH", "pattern matching"), ("Variable-length path", "k-hop traversal")]),
"quiz": quiz("p9-l06-graph-queries",
    sq("q1", "MATCH (a)-[:KNOWS]->(b)…", ["Directed pattern", "INSERT only", "DROP", "VACUUM"], 0, "Pattern syntax."),
    sq("q2", "[:FRIEND*1..3]…", ["1 to 3 hops", "Exactly 1", "Infinite only", "No path"], 0, "Variable length."),
    sq("q3", "RETURN in Cypher…", ["Output columns", "Delete all", "Create index", "Grant"], 0, "Projection."),
    sq("q4", "Deep traversal SQL…", ["Recursive CTE", "Simple JOIN once", "TRUNCATE", "TOAST"], 0, "SQL recursion."),
    mq("q5", "Cypher patterns? (верные)", ["Node label :Student", "Relationship :KNOWS", "Property filter {name:'X'}", "TABLESPACE"], [0,1,2], "Cypher elements.")),
"tasks": """## Задания (опционально — Neo4j sandbox)

1. Cypher: все курсы студента Иванов.
2. 2-hop friends of Alice.
3. SQL recursive equivalent для 2-hop.
4. Когда JOIN 10 tables хуже graph traversal?""",
}

LESSONS["p9-l07-tsql-overview"] = {
"md": md("T-SQL: обзор для PostgreSQL-разработчика", P9, M9B,
    CMP + "\nПрактика: сравнение синтаксиса; PostgreSQL — основная среда курса.",
    ["Сопоставить синтаксис T-SQL и PostgreSQL", "Использовать TOP и OFFSET/FETCH", "Применить переменные и batch"],
    """**T-SQL** — диалект Microsoft SQL Server. Курс использует PostgreSQL; этот урок — **сравнение диалектов**.

| Задача | T-SQL | PostgreSQL |
|--------|-------|------------|
| Top N | `SELECT TOP 10 * FROM t` | `SELECT * FROM t LIMIT 10` |
| Pagination | `OFFSET 10 ROWS FETCH NEXT 5 ROWS ONLY` | `LIMIT 5 OFFSET 10` |
| String concat | `'a' + 'b'` | `'a' \|\| 'b'` or concat() |
| Identity | `IDENTITY(1,1)` | `SERIAL` / `GENERATED ALWAYS AS IDENTITY` |
| Boolean | `BIT` | `BOOLEAN` |
| Date | `GETDATE()` | `now()` / `CURRENT_TIMESTAMP` |
| Batch | `GO` separator | Single transaction / `;` |

**Variables:**
```sql
-- T-SQL
DECLARE @x INT = 5;
-- PostgreSQL
DO $$ DECLARE x int := 5; BEGIN ... END $$;
```

**Schemas:** SQL Server dbo vs PostgreSQL public.""",
    [("ben-gan", "Главы 1–3"), ("petkovic", "Главы 1–4")],
    [("TOP", "T-SQL limit rows"), ("LIMIT", "PostgreSQL limit"), ("GO", "batch separator SSMS"),
     ("IDENTITY", "auto-increment T-SQL")]),
"quiz": quiz("p9-l07-tsql-overview",
    sq("q1", "TOP 10 in T-SQL ≈ PG…", ["LIMIT 10", "OFFSET 10", "FETCH WAL", "TOP is PG native"], 0, "LIMIT equivalent."),
    sq("q2", "GETDATE() in PG…", ["now() or CURRENT_TIMESTAMP", "GETDATE()", "SYSDATE only", "No dates"], 0, "Timestamp functions."),
    sq("q3", "GO in SSMS…", ["Batch separator not SQL", "Transaction commit", "CREATE INDEX", "RLS"], 0, "Client directive."),
    sq("q4", "IDENTITY ≈ PG…", ["SERIAL / GENERATED IDENTITY", "UUID only", "MANUAL only", "TOAST"], 0, "Auto increment."),
    mq("q5", "Dialect diffs? (верные)", ["TOP vs LIMIT", "+ vs \|\| concat", "BIT vs BOOLEAN", "Identical MERGE syntax always"], [0,1,2], "Compare dialects.")),
"tasks": """## Задания — сравнение диалектов

""" + CMP + """
1. Перепишите T-SQL `SELECT TOP 5 name FROM student ORDER BY name` → PostgreSQL.
2. Pagination: OFFSET/FETCH (T-SQL) vs LIMIT/OFFSET (PG) — один запрос, два варианта.
3. DECLARE variable: напишите оба синтаксиса.
4. Таблица: 5 отличий T-SQL vs PostgreSQL из опыта.""",
}

LESSONS["p9-l08-tsql-advanced"] = {
"md": md("T-SQL: процедуры, функции и MERGE", P9, M9B,
    CMP + "\nСравнение продвинутых конструкций T-SQL и PostgreSQL.",
    ["Написать stored procedure в T-SQL", "Использовать MERGE для upsert", "Применить error handling TRY/CATCH"],
    """**Stored procedures:**

```sql
-- T-SQL
CREATE PROC dbo.UpsertGrade @sid INT, @grade INT AS
BEGIN TRY
  MERGE performance AS t USING (SELECT @sid AS sid) s ON t.student_id = s.sid
  WHEN MATCHED THEN UPDATE SET grade = @grade
  WHEN NOT MATCHED THEN INSERT (student_id, grade) VALUES (@sid, @grade);
END TRY
BEGIN CATCH
  THROW;
END CATCH

-- PostgreSQL
CREATE OR REPLACE PROC upsert_grade(p_sid int, p_grade int)
LANGUAGE plpgsql AS $$
BEGIN
  INSERT INTO performance (student_id, grade) VALUES (p_sid, p_grade)
  ON CONFLICT (student_id) DO UPDATE SET grade = EXCLUDED.grade;
EXCEPTION WHEN OTHERS THEN RAISE;
END; $$;
```

| Feature | T-SQL | PostgreSQL |
|---------|-------|------------|
| MERGE | Native MERGE (2019+) | INSERT ON CONFLICT |
| Error handling | TRY/CATCH | EXCEPTION block |
| Procedures | CREATE PROC | CREATE PROCEDURE (PG14+) |
| Table variables | @t TABLE | TEMP TABLE |
| Output inserted | OUTPUT clause | RETURNING |""",
    [("ben-gan", "Главы 10–11"), ("pro-tsql", "Главы 5–7")],
    [("MERGE", "upsert T-SQL"), ("ON CONFLICT", "upsert PostgreSQL"),
     ("TRY/CATCH", "T-SQL errors"), ("RETURNING", "PG output clause")]),
"quiz": quiz("p9-l08-tsql-advanced",
    sq("q1", "MERGE in PG often replaced by…", ["INSERT ON CONFLICT", "TOP 10", "CROSS JOIN", "VACUUM"], 0, "Upsert pattern."),
    sq("q2", "TRY/CATCH ≈ PG…", ["BEGIN ... EXCEPTION", "Only GO", "pg_hba", "WAL"], 0, "Exception handling."),
    sq("q3", "OUTPUT inserted in T-SQL ≈…", ["RETURNING in PG", "LIMIT", "TOAST", "RLS"], 0, "Returning rows."),
    sq("q4", "CREATE PROC in PG since…", ["v14+ procedures", "Never", "Only Mongo", "v8 only"], 0, "SQL procedures."),
    mq("q5", "Upsert options? (верные)", ["T-SQL MERGE", "PG ON CONFLICT", "Manual IF EXISTS", "Only TRUNCATE"], [0,1,2], "Upsert patterns.")),
"tasks": """## Задания — сравнение диалектов

""" + CMP + """
1. MERGE/upsert grade для student_id — T-SQL и PG версии.
2. TRY/CATCH (T-SQL) vs EXCEPTION (PG) — пример деления на ноль.
3. OUTPUT vs RETURNING после INSERT.
4. Когда портировать proc с T-SQL на PL/pgSQL — checklist (5 пунктов).""",
}

LESSONS["p9-l09-date-advanced"] = {
"md": md("К. Дж. Дейт: продвинутая реляционная теория", P9, M9B, TH,
    ["Обсудить NULL и реляционную модель", "Разобрать view updating problem", "Оценить соответствие SQL теории"],
    """**К. Дж. Дейт** критически оценивает SQL с позиции реляционной теории.

**NULL:** SQL ternary logic (TRUE/FALSE/UNKNOWN); Date: NULL нарушает информационную целостность — «missing» vs «not applicable»; рекомендация — избегать NULL, использовать домены и DEFAULT или отдельные таблицы.

**View updating problem:** не все VIEW обновляемы; JOIN view, aggregation view — неоднозначность какую base table обновлять. SQL1999+ CHECK OPTION, INSTEAD OF triggers; PostgreSQL — rules, triggers.

**Duplicate rows:** SQL bag semantics (multiset) vs relational set; DISTINCT «латание».

**Foreign key actions:** theory vs CASCADE практика.

**The Third Manifesto / Tutorial D:** альтернатива SQL (не промышленный стандарт, но учит мыслить реляционно).

**PostgreSQL:** близок к SQL standard, но extensions (JSONB, arrays) — pragmatic departure.

Читать: Date «SQL and Relational Theory», главы о NULL, views, constraints.""",
    [("date-sql", "Главы 11–14"), ("date-intro", "Главы 19–21")],
    [("NULL problem", "трёхзначная логика"), ("View updating", "обновление представлений"),
     ("Bag vs set", "дубликаты в SQL"), ("Relational fidelity", "соответствие теории")]),
"quiz": quiz("p9-l09-date-advanced",
    sq("q1", "Date criticizes NULL because…", ["Ambiguous meaning", "Too fast", "No indexes", "WAL"], 0, "Semantic ambiguity."),
    sq("q2", "View with GROUP BY update…", ["Generally not updatable", "Always simple", "Auto MERGE", "Mongo only"], 0, "Updating problem."),
    sq("q3", "SQL bags vs sets…", ["SQL allows duplicates without DISTINCT", "SQL is always set", "No difference", "PG only"], 0, "Multiset semantics."),
    sq("q4", "INSTEAD OF trigger helps…", ["Updatable complex views", "Backup", "Replication", "TOAST"], 0, "View update workaround."),
    mq("q5", "Date themes? (верные)", ["NULL critique", "View updating", "Relational purity", "Replace all SQL with Mongo"], [0,1,2], "Theory topics.")),
"tasks": """## Задания

1. Пример WHERE unknown (NULL comparison) — SQL behavior.
2. Создайте VIEW с JOIN — почему INSERT ambiguous?
3. DISTINCT: когда «костыль» vs legitimate?
4. Date гл. 11–14: 3 тезиса своими словами.
5. PostgreSQL JSONB — departure from pure relational? аргументы.""",
}

LESSONS["p9-l10-exam"] = {
"md": md("Итоговый контроль: альтернативные СУБД и теория", P9, M9B, EX,
    ["Выбрать СУБД под задачу", "Написать запросы MongoDB и Cypher", "Подвести итоги курса"],
    """**Итог курса:** реляционная теория → проектирование → SQL → performance → PostgreSQL internals → admin → DWH → NoSQL/graph/T-SQL/Date.

**Сценарии выбора СУБД:**
- OLTP university → PostgreSQL
- Analytics grades → DWH star schema
- Flexible catalog → MongoDB or JSONB
- Social/fraud paths → Graph DB
- MS stack shop → T-SQL; cloud neutral → PostgreSQL

Сравнение диалектов T-SQL↔PG, theory Date для критического мышления.""",
    [("mongodb", "Главы 1–7 (повторение)"), ("graph-db", "Главы 1–5 (повторение)"), ("date-sql", "Главы 11–14 (повторение)")],
    [("Polyglot persistence", "разные БД под задачи"), ("Document model", "MongoDB"),
     ("Graph traversal", "Cypher"), ("Relational theory", "Date")]),
"quiz": quiz("p9-l10-exam",
    sq("q1", "University OLTP best…", ["PostgreSQL ACID", "Mongo only", "Graph only", "No DB"], 0, "OLTP relational."),
    sq("q2", "6-hop friends…", ["Graph DB", "CSV", "pg_hba", "TOAST"], 0, "Traversal workload."),
    sq("q3", "T-SQL TOP → PG…", ["LIMIT", "MERGE", "VACUUM", "RLS"], 0, "Dialect map."),
    sq("q4", "Star schema for grades…", ["DWH analytics", "OLTP only", "WAL", "Auth"], 0, "Dimensional DWH."),
    mq("q5", "Course finale topics? (верные)", ["NoSQL models", "Graph Cypher", "T-SQL vs PG", "Only Part 0"], [0,1,2], "Part 9 recap.")),
"tasks": """## Итоговая аттестация

1. **Выбор СУБД:** 4 сценария (OLTP, DWH, catalog, social) — обоснуйте выбор.
2. Mongo: find + aggregation ИЛИ псевдокод (без установки).
3. Cypher: MATCH 2-hop path (на бумаге).
4. T-SQL vs PG: 5 пар конструкций.
5. Date: эссе NULL (½ стр.).
6. Рефлексия курса: что изучили, что примените.
7. Все тесты части 9 ≥70%.""",
}

## Шифрование: at rest и in transit

**Часть:** Администрирование и архитектуры нагрузок · **Модуль:** Безопасность и эксплуатация

Фокус на теории и тесте; SQL не обязателен.

### Цели урока

- Настроить SSL для подключений
- Объяснить TDE и pgcrypto
- Выбрать стратегию защиты данных

### Краткая теория

**In transit:** TLS между клиентом и PostgreSQL (`ssl=on`, `hostssl` в pg_hba). Защита от перехвата паролей/данных в сети.

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

**CAP-контекст:** шифрование не заменяет backup/replication; согласованность и доступность — отдельные оси.

### Что читать в источниках

1. **1-я очередь.** Новиков Б. А. и др. — Основы технологий баз данных — Глава 15, §15.2
2. **2-я очередь.** Комаров В. И. — Путеводитель по базам данных — Раздел 14: шифрование
### Ключевые понятия

- **TLS** — шифрование канала.
- **At rest** — шифрование на диске.
- **pgcrypto** — шифрование столбцов.
- **TDE** — прозрачное шифрование БД.

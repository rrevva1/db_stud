## Write-Ahead Log и контрольные точки

**Часть:** Внутреннее устройство PostgreSQL · **Модуль:** Хранение и расширения

Фокус на теории и тесте; SQL не обязателен.

### Цели урока

- Объяснить назначение WAL
- Настроить checkpoint и wal_level
- Понять crash recovery

### Краткая теория

**WAL:** сначала запись в журнал, затем в data-файлы. COMMIT подтверждается после fsync WAL.

Сегменты в `pg_wal/` (~16 МБ). **Checkpoint** сбрасывает dirty buffers, позволяет recycle WAL. Параметры: `checkpoint_timeout`, `max_wal_size`, `checkpoint_completion_target`.

**Crash recovery:** redo WAL с последнего checkpoint; незавершённые TX — rollback.

| wal_level | Применение |
|-----------|------------|
| minimal | Только recovery |
| replica | Streaming replication, base backup |
| logical | Logical replication |

WAL — основа **репликации** и **PITR** (point-in-time recovery).

### Что читать в источниках

1. **1-я очередь.** Моргунов Е. П. — PostgreSQL. Основы языка SQL — Глава 18, §18.3
2. **2-я очередь.** Новиков Б. А. и др. — Основы технологий баз данных — Глава 13, §13.2
### Ключевые понятия

- **WAL** — журнал упреждающей записи.
- **Checkpoint** — точка сброса на диск.
- **LSN** — Log Sequence Number.
- **Redo** — повтор изменений при recovery.

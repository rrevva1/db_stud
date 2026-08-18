-- p5-l06-functions-plpgsql.sql
-- Функции и процедуры PL/pgSQL (UTF-8)
-- Практика: хранимая логика для отчётов, триггеров, динамического SQL

-- Скalarная функция: стипендия по среднему баллу
CREATE OR REPLACE FUNCTION fn_scholarship_amount(p_avg_grade numeric)
RETURNS numeric
LANGUAGE plpgsql
IMMUTABLE
AS $$
BEGIN
    IF p_avg_grade IS NULL THEN
        RETURN 0;
    ELSIF p_avg_grade >= 4.5 THEN
        RETURN 15000;
    ELSIF p_avg_grade >= 4.0 THEN
        RETURN 10000;
    ELSIF p_avg_grade >= 3.5 THEN
        RETURN 5000;
    ELSE
        RETURN 0;
    END IF;
END;
$$;

SELECT fn_scholarship_amount(4.6), fn_scholarship_amount(3.2);

-- Функция, возвращающая таблицу (отчёт)
CREATE OR REPLACE FUNCTION fn_top_students(p_limit int DEFAULT 5)
RETURNS TABLE(student_id int, avg_grade numeric)
LANGUAGE plpgsql
STABLE
AS $$
BEGIN
    RETURN QUERY
    SELECT p.student_id, avg(p.grade)::numeric(4,2)
    FROM performance p
    GROUP BY p.student_id
    ORDER BY avg(p.grade) DESC
    LIMIT p_limit;
END;
$$;

-- Процедура (PostgreSQL 11+): транзакция внутри CALL
CREATE OR REPLACE PROCEDURE proc_grant_scholarship(p_student_id int, p_amount numeric)
LANGUAGE plpgsql
AS $$
BEGIN
    -- пример: upsert в таблицу стипендий (создайте при необходимости)
    RAISE NOTICE 'Стипендия % для студента %', p_amount, p_student_id;
END;
$$;

-- Триггерная функция: аудит изменений
CREATE TABLE IF NOT EXISTS audit_log (
    id         bigserial PRIMARY KEY,
    table_name text,
    operation  text,
    changed_at timestamptz DEFAULT now(),
    old_data   jsonb,
    new_data   jsonb
);

CREATE OR REPLACE FUNCTION trg_audit_fn()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, operation, new_data)
        VALUES (TG_TABLE_NAME, TG_OP, to_jsonb(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, operation, old_data, new_data)
        VALUES (TG_TABLE_NAME, TG_OP, to_jsonb(OLD), to_jsonb(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, operation, old_data)
        VALUES (TG_TABLE_NAME, TG_OP, to_jsonb(OLD));
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$;

-- Пример: функция для создания месячной секции (partition helper)
CREATE OR REPLACE FUNCTION fn_create_month_partition(
    p_parent regclass,
    p_year int,
    p_month int
) RETURNS void
LANGUAGE plpgsql
AS $$
DECLARE
    v_start date := make_date(p_year, p_month, 1);
    v_end   date := (v_start + interval '1 month')::date;
    v_name  text := format('%s_y%sm%s', p_parent::text, p_year, lpad(p_month::text, 2, '0'));
    v_sql   text;
BEGIN
    v_sql := format(
        'CREATE TABLE IF NOT EXISTS %I PARTITION OF %s FOR VALUES FROM (%L) TO (%L)',
        v_name, p_parent, v_start, v_end
    );
    EXECUTE v_sql;
    RAISE NOTICE 'Создана секция: %', v_name;
END;
$$;

-- Безопасный динамический SQL с format/quote_ident (см. p5-l08, p5-l09)
CREATE OR REPLACE FUNCTION fn_table_row_count(p_schema text, p_table text)
RETURNS bigint
LANGUAGE plpgsql
STABLE
AS $$
DECLARE
    v_count bigint;
BEGIN
    EXECUTE format(
        'SELECT count(*)::bigint FROM %I.%I',
        p_schema, p_table
    ) INTO v_count;
    RETURN v_count;
END;
$$;

-- SELECT fn_table_row_count('public', 'student');

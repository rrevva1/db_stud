-- p3-l02-insert-select.sql
-- INSERT и SELECT на схеме university

SET search_path TO university, public;

-- Одна строка
INSERT INTO faculty (name, short_name)
VALUES ('Факультет информатики', 'ФИ')
RETURNING faculty_id, name;

-- Несколько строк
INSERT INTO s_group (name, faculty_id, course_num, entry_year) VALUES
    ('ИВТ-21', 1, 3, 2021),
    ('ИВТ-22', 1, 2, 2022),
    ('ПМИ-21', 1, 3, 2021);

INSERT INTO student (last_name, first_name, birth_date, email) VALUES
    ('Иванов', 'Пётр', '2003-05-12', 'ivanov@uni.local'),
    ('Петрова', 'Анна', '2004-01-20', 'petrova@uni.local');

INSERT INTO student_in_group (student_id, group_id)
SELECT s.student_id, g.group_id
FROM student s, s_group g
WHERE s.last_name = 'Иванов' AND g.name = 'ИВТ-21';

-- Базовый SELECT
SELECT student_id, last_name, first_name
FROM student
ORDER BY last_name;

SELECT s.last_name, g.name AS group_name
FROM student s
JOIN student_in_group sig ON sig.student_id = s.student_id
JOIN s_group g ON g.group_id = sig.group_id;

-- p3-l14-joins.sql
-- INNER JOIN: студенты и группы

SET search_path TO university, public;

-- Две таблицы
SELECT s.last_name, s.first_name, g.name AS group_name, g.course_num
FROM student s
INNER JOIN student_in_group sig ON sig.student_id = s.student_id
INNER JOIN s_group g ON g.group_id = sig.group_id
WHERE g.course_num = 3
ORDER BY g.name, s.last_name;

-- Три таблицы: оценки
SELECT s.last_name, subj.name AS subject, p.grade, p.grade_date
FROM performance p
JOIN student s ON s.student_id = p.student_id
JOIN subject subj ON subj.subject_id = p.subject_id
WHERE p.grade >= 4;

-- Эквивалент через WHERE (устаревший стиль)
SELECT s.last_name, g.name
FROM student s, student_in_group sig, s_group g
WHERE sig.student_id = s.student_id AND g.group_id = sig.group_id;

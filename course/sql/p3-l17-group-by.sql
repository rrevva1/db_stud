-- p3-l17-group-by.sql
-- GROUP BY и агрегатные функции

SET search_path TO university, public;

-- Средний балл по дисциплинам
SELECT subj.name,
       COUNT(*) AS grades_count,
       ROUND(AVG(p.grade)::numeric, 2) AS avg_grade,
       MIN(p.grade) AS min_grade,
       MAX(p.grade) AS max_grade
FROM performance p
JOIN subject subj ON subj.subject_id = p.subject_id
GROUP BY subj.name
ORDER BY avg_grade DESC;

-- Количество студентов в каждой группе
SELECT g.name, COUNT(sig.student_id) AS students_cnt
FROM s_group g
LEFT JOIN student_in_group sig ON sig.group_id = g.group_id
GROUP BY g.group_id, g.name
HAVING COUNT(sig.student_id) > 0;

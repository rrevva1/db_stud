-- p3-l19-subqueries.sql
-- Скalar, IN, EXISTS

SET search_path TO university, public;

-- Скalar: средний балл для сравнения
SELECT s.last_name, subj.name, p.grade
FROM performance p
JOIN student s ON s.student_id = p.student_id
JOIN subject subj ON subj.subject_id = p.subject_id
WHERE p.grade > (
    SELECT AVG(grade) FROM performance
);

-- IN: студенты из группы ИВТ-21
SELECT last_name, first_name
FROM student
WHERE student_id IN (
    SELECT sig.student_id
    FROM student_in_group sig
    JOIN s_group g ON g.group_id = sig.group_id
    WHERE g.name = 'ИВТ-21'
);

-- EXISTS: дисциплины, по которым есть оценки
SELECT name FROM subject subj
WHERE EXISTS (
    SELECT 1 FROM performance p WHERE p.subject_id = subj.subject_id
);

-- Подзапрос во FROM
SELECT g.name, stats.avg_grade
FROM s_group g
JOIN (
    SELECT sig.group_id, AVG(p.grade) AS avg_grade
    FROM student_in_group sig
    JOIN performance p ON p.student_id = sig.student_id
    GROUP BY sig.group_id
) stats ON stats.group_id = g.group_id;

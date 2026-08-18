-- p3-l22-lab-university.sql
-- Полная лабораторная схема «Университет» + тестовые данные
-- Выполните после schema-university.sql или самостоятельно

\\i schema-university.sql

SET search_path TO university, public;

INSERT INTO faculty (name, short_name) VALUES
    ('Факультет информатики', 'ФИ'),
    ('Факультет математики', 'ФМ');

INSERT INTO s_group (name, faculty_id, course_num, entry_year) VALUES
    ('ИВТ-21', 1, 3, 2021),
    ('ИВТ-22', 1, 2, 2022),
    ('ПМИ-21', 2, 3, 2021);

INSERT INTO student (last_name, first_name, middle_name, birth_date, email) VALUES
    ('Иванов', 'Пётр', 'Сергеевич', '2003-05-12', 'ivanov@uni.local'),
    ('Петрова', 'Анна', 'Игоревна', '2004-01-20', 'petrova@uni.local'),
    ('Сидоров', 'Олег', NULL, '2003-11-03', 'sidorov@uni.local'),
    ('Козлова', 'Мария', 'Андреевна', '2004-07-15', NULL);

INSERT INTO student_in_group (student_id, group_id) VALUES
    (1, 1), (2, 1), (3, 2), (4, 3);

INSERT INTO teacher (last_name, first_name, degree) VALUES
    ('Смирнов', 'Алексей', 'доцент'),
    ('Кузнецова', 'Елена', 'профессор');

INSERT INTO subject (name, hours) VALUES
    ('Базы данных', 72),
    ('Алгоритмы', 108),
    ('Математический анализ', 144);

INSERT INTO performance (student_id, subject_id, teacher_id, grade_date, grade) VALUES
    (1, 1, 1, '2024-01-15', 5),
    (1, 2, 1, '2024-02-01', 4),
    (2, 1, 1, '2024-01-15', 5),
    (2, 3, 2, '2024-03-10', 4),
    (3, 1, 1, '2024-01-15', 3),
    (4, 3, 2, '2024-03-10', 5);

-- Контрольные запросы
SELECT g.name, COUNT(DISTINCT sig.student_id) AS cnt
FROM s_group g
LEFT JOIN student_in_group sig ON sig.group_id = g.group_id
GROUP BY g.name;

SELECT s.last_name, AVG(p.grade)::numeric(4,2) AS avg_grade
FROM student s
JOIN performance p ON p.student_id = s.student_id
GROUP BY s.student_id, s.last_name
HAVING AVG(p.grade) >= 4.5;

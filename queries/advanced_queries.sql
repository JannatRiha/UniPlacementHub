-- 1. CSE students with CGPA >= 3.3 who applied to remote internships in the last 7 days.
SELECT s.full_name, s.cgpa, d.name AS department, p.title, a.applied_at
FROM applications_application a
JOIN students_student s ON a.student_id = s.user_id
JOIN students_department d ON s.department_id = d.id
JOIN postings_posting p ON a.posting_id = p.id
WHERE d.name = 'CSE'
  AND s.cgpa >= 3.30
  AND p.is_remote = TRUE
  AND p.type = 'internship'
  AND a.applied_at >= CURRENT_TIMESTAMP - INTERVAL '7 days';

-- 2. Postings with more applicants than available positions.
SELECT p.id, p.title, p.positions, COUNT(a.id) AS applicant_count
FROM postings_posting p
LEFT JOIN applications_application a ON a.posting_id = p.id
GROUP BY p.id, p.title, p.positions
HAVING COUNT(a.id) > p.positions;

-- 3. Skill matches for a student.
SELECT p.id, p.title, COUNT(ps.skill_id) AS matching_skills
FROM postings_posting p
JOIN postings_posting_skills ps ON ps.posting_id = p.id
JOIN students_student_skills ss ON ss.skill_id = ps.skill_id
WHERE ss.student_id = 1
GROUP BY p.id, p.title
ORDER BY matching_skills DESC;

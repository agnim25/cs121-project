SELECT link
FROM publications NATURAL JOIN mentors
WHERE department_name = 'Computing and Mathematical Sciences'
ORDER BY publication_date;

SELECT mentor_name
FROM mentor
WHERE department_name = 'Computing and Mathematical Sciences'
AND is_surf = 1;

SELECT link
FROM publications
WHERE mentor_id = (
    SELECT mentor_id
    FROM mentors
    WHERE mentor_name = 'Johnny Appleseed'
)
ORDER BY publication_date;

SELECT mentor_name
FROM mentor
WHERE department_name = 'EAS'
ORDER BY publication_date;

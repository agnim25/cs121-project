SET SESSION group_concat_max_len = 100000;

-- Authenticate a user when logging in
SELECT authenticate('damonlin', 'qwerty') AS result;

-- Determine whether the user is a mentor or a student
SELECT user_type FROM users WHERE user_id = 1;

-- Find the corresponding user_id for a mentor
SELECT user_id FROM users
WHERE email = 'dllin@caltech.edu'
AND user_type = 'mentor';

-- Selects keywords and abstracts into a single description for each mentor
SELECT 
    kw.user_id AS user_id, 
    kw.keywords AS keywords, 
    ab.abstracts AS abstracts
FROM
    (SELECT u.user_id, GROUP_CONCAT(k.keyword SEPARATOR ' ') AS keywords
    FROM mentors u
    JOIN keywords k ON u.user_id = k.user_id
    WHERE u.interests_last_updated IS NOT NULL
    GROUP BY u.user_id) AS kw
JOIN
    (SELECT u.user_id, GROUP_CONCAT(p.abstract SEPARATOR ' ') AS abstracts
    FROM mentors u
    JOIN publications p ON u.user_id = p.user_id
    WHERE u.interests_last_updated IS NOT NULL AND p.abstract IS NOT NULL
    GROUP BY u.user_id) AS ab
ON kw.user_id = ab.user_id;

-- Update the user embedding vector
UPDATE users
SET embedding_vector = '[0, 1, 0]'
WHERE user_id = 1000;

-- Update the last updated time of mentor interest to NULL
UPDATE mentors
SET interests_last_updated = NULL
WHERE user_id = 1000;

-- Get the embedding vector of a user
SELECT embedding_vector FROM users WHERE user_id = 1000;

-- Get user id and embedding vector of all mentors
SELECT user_id, embedding_vector FROM users WHERE user_type = 'mentor';

-- Get all publication links of a mentor ordered by publication date
SELECT link FROM publications WHERE user_id = 2 ORDER BY publication_date;

-- Get all mentors in EE taking students for SURF
SELECT name FROM users NATURAL JOIN mentors
WHERE user_type = 'mentor'
AND surf = 1
AND department = 'Electrical Engineering';

-- Get all mentors in EE taking students for academic year research
SELECT name FROM users NATURAL JOIN mentors
WHERE user_type = 'mentor'
AND academic_year = 1
AND department = 'Electrical Engineering';

-- Get all mentors in EE
SELECT name FROM users NATURAL JOIN mentors
WHERE user_type = 'mentor'
AND department = 'Electrical Engineering';

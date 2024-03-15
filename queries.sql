-- Authenticate a user when logging in
SELECT authenticate('damonlin', 'qwerty') AS result

-- Determine whether the user is a mentor or a student
SELECT user_type FROM users WHERE user_id = 1;

-- Find the corresponding user_id for a mentor
SELECT user_id FROM users
WHERE email = 'dllin@caltech.edu'
AND user_type = \'mentor\';

-- 
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

UPDATE users
SET embedding_vector = '[0, 1, 0]'
WHERE user_id = 1000;

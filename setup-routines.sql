DROP FUNCTION IF EXISTS calculate_total_citations;
DROP FUNCTION IF EXISTS calculate_h_index;
DROP PROCEDURE IF EXISTS add_client;
DROP PROCEDURE IF EXISTS add_student_research_statement;
DROP PROCEDURE IF EXISTS add_keyword;
DROP PROCEDURE IF EXISTS add_mentor;
DROP TRIGGER IF EXISTS after_publications_insert;
DROP TRIGGER IF EXISTS after_keywords_insert;

-- udfs

-- calculate total citations of a mentor based on stored publications
DELIMITER !
CREATE FUNCTION calculate_total_citations(user_id INT) RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE total_citations INT;
    SELECT SUM(citations) INTO total_citations FROM publications WHERE user_id = user_id;
    RETURN total_citations;
END !
DELIMITER ;

-- calculate h-index of a mentor based on stored publications
DELIMITER !
CREATE FUNCTION calculate_h_index(user_id INT) RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE h_index INT DEFAULT 0;
    DECLARE done INT DEFAULT FALSE;
    DECLARE citations INT;
    DECLARE n INT DEFAULT 0;
    DECLARE cur CURSOR FOR SELECT citations FROM publications WHERE user_id = user_id ORDER BY citations DESC;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    h_index_loop: LOOP
        FETCH cur INTO citations;
        IF done THEN
            LEAVE h_index_loop;
        END IF;
        SET n = n + 1;
        IF citations < n THEN
            SET h_index = n - 1;
            LEAVE h_index_loop;
        END IF;
    END LOOP;

    CLOSE cur;
    RETURN h_index;
END !
DELIMITER ;


-- procedures
DELIMITER !
CREATE PROCEDURE add_client(
    IN p_name VARCHAR(50),
    IN p_email VARCHAR(50),
    IN p_year YEAR,
    IN p_surf TINYINT,
    IN p_academic_year TINYINT,
    IN p_user_type VARCHAR(50),
    IN p_vector TEXT,
    OUT p_user_id INT
)
BEGIN
    -- Check if the user already exists based on email
    IF NOT EXISTS (SELECT 1 FROM users WHERE email = p_email) THEN
        -- Insert the new user
        INSERT INTO users(name, email, year, surf, academic_year, user_type, embedding_vector)
        VALUES (p_name, p_email, p_year, p_surf, p_academic_year, p_user_type, p_vector);
        
        -- Set the OUT parameter to the last inserted id
        SET p_user_id = LAST_INSERT_ID();
    ELSE
        -- If user exists, return a user_id of NULL or another indicative value
        SET p_user_id = NULL;
    END IF;
END !
DELIMITER ;

DELIMITER !
CREATE PROCEDURE add_student_research_statement(
    IN p_user_id INT,
    IN p_research_statement TEXT
)
BEGIN
    -- Check if a statement already exists for the user and update or insert accordingly
    IF EXISTS (SELECT 1 FROM student_research_statements WHERE user_id = p_user_id) THEN
        UPDATE student_research_statements
        SET research_statement = p_research_statement
        WHERE user_id = p_user_id;
    ELSE
        INSERT INTO student_research_statements(user_id, research_statement)
        VALUES (p_user_id, p_research_statement);
    END IF;
END !
DELIMITER ;

DELIMITER !
CREATE PROCEDURE add_keyword(
    IN p_user_id INT,
    IN p_keyword VARCHAR(100)
)
BEGIN 
    INSERT INTO keywords(user_id, keyword)
    VALUES (p_user_id, p_keyword);
END !
DELIMITER ;

DELIMITER !
CREATE PROCEDURE add_mentor(
    IN p_user_id INT,
    IN p_department VARCHAR(100),
    IN p_principal_investigator VARCHAR(100)
)
BEGIN 
    INSERT INTO mentors(user_id, department, principal_investigator, interests_last_updated)
    VALUES (p_user_id, p_department, p_principal_investigator, GETDATE());
END !
DELIMITER ;


-- triggers
DELIMITER !
CREATE TRIGGER after_publications_insert
AFTER INSERT ON publications
FOR EACH ROW
BEGIN
    UPDATE mentors
    SET interests_last_updated = CURRENT_DATE()
    WHERE user_id = NEW.user_id;
END !
DELIMITER ;

DELIMITER !
CREATE TRIGGER after_keywords_insert
AFTER INSERT ON keywords
FOR EACH ROW
BEGIN
    UPDATE mentors
    SET interests_last_updated = CURRENT_DATE()
    WHERE user_id = NEW.user_id;
END !
DELIMITER ;

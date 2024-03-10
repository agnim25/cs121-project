DROP FUNCTION IF EXISTS make_salt;
DELIMITER !
CREATE FUNCTION make_salt(num_chars INT)
RETURNS VARCHAR(20) DETERMINISTIC
BEGIN
    DECLARE salt VARCHAR(20) DEFAULT '';

    -- Don't want to generate more than 20 characters of salt.
    SET num_chars = LEAST(20, num_chars);

    -- Generate the salt!  Characters used are ASCII code 32 (space)
    -- through 126 ('z').
    WHILE num_chars > 0 DO
        SET salt = CONCAT(salt, CHAR(32 + FLOOR(RAND() * 95)));
        SET num_chars = num_chars - 1;
    END WHILE;

    RETURN salt;
END !
DELIMITER ;

DROP TABLE IF EXISTS user_info;
CREATE TABLE user_info (
    -- Usernames are up to 20 characters.
    username VARCHAR(20) PRIMARY KEY,

    -- Salt will be 8 characters all the time, so we can make this 8.
    salt CHAR(8) NOT NULL,

    -- We use SHA-2 with 256-bit hashes.  MySQL returns the hash
    -- value as a hexadecimal string, which means that each byte is
    -- represented as 2 characters.  Thus, 256 / 8 * 2 = 64.
    -- We can use BINARY or CHAR here; BINARY simply has a different
    -- definition for comparison/sorting than CHAR.
    password_hash BINARY(64) NOT NULL
);

-- Adds a new user to the user_info table, using the specified password (max
-- of 20 characters). Salts the password with a newly-generated salt value,
-- and then the salt and hash values are both stored in the table.
DROP PROCEDURE IF EXISTS sp_add_user;
DELIMITER !
CREATE PROCEDURE sp_add_user(new_username VARCHAR(20), password VARCHAR(20))
BEGIN
  DECLARE salt1        CHAR(8);
  DECLARE new_password VARCHAR(64);
  SET salt1 = make_salt(8);
  SET new_password = SHA2(CONCAT(salt1, password), 256);
  INSERT INTO user_info VALUES (new_username, salt1, new_password);
END !
DELIMITER ;

-- Authenticates the specified username and password against the data
-- in the user_info table.  Returns 1 if the user appears in the table, and the
-- specified password hashes to the value for the user. Otherwise returns 0.
DROP FUNCTION IF EXISTS authenticate;
DELIMITER !
CREATE FUNCTION authenticate(username VARCHAR(20), password VARCHAR(20))
RETURNS TINYINT DETERMINISTIC
BEGIN
  DECLARE salt_password   VARCHAR(28);
  DECLARE new_password    VARCHAR(64);
  DECLARE actual_password VARCHAR(64);
  IF username NOT IN (SELECT username FROM user_info) THEN
    RETURN 0;
  END IF;
  SET salt_password = (SELECT salt FROM user_info
    WHERE username = user_info.username);
  SET new_password = SHA2(CONCAT(salt_password, password), 256);
  SET actual_password = (SELECT password_hash FROM user_info
    WHERE username = user_info.username);
  IF actual_password = new_password THEN
    RETURN 1;
  END IF;
  RETURN 0;
END !
DELIMITER ;

-- Create a procedure sp_change_password to generate a new salt and change the given
-- user's password to the given password (after salting and hashing)
DROP PROCEDURE IF EXISTS sp_change_password;
DELIMITER !
CREATE PROCEDURE sp_change_password(username VARCHAR(20), new_password VARCHAR(20))
BEGIN
  DECLARE salt1         VARCHAR(28);
  DECLARE new_password1 VARCHAR(64);
  SET salt1 = make_salt(8);
  SET new_password1 = SHA2(CONCAT(salt1, new_password), 256);
  UPDATE user_info SET salt = salt1, password_hash = new_password1
    WHERE username = user_info.username;
END !
DELIMITER ;

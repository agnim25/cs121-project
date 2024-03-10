DROP USER IF EXISTS 'admin'@'localhost';
DROP USER IF EXISTS 'client'@'localhost';

CREATE USER 'admin'@'localhost' IDENTIFIED BY 'adminpw';
CREATE USER 'client'@'localhost' IDENTIFIED BY 'clientpw';

GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost';
GRANT SELECT ON cs121project.* TO 'client'@'localhost';
GRANT EXECUTE ON PROCEDURE cs121project.sp_add_user TO 'client'@'localhost';
GRANT EXECUTE ON FUNCTION cs121project.authenticate TO 'client'@'localhost';

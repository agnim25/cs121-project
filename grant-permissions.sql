DROP USER IF EXISTS 'admin'@'localhost';
DROP USER IF EXISTS 'client'@'localhost';

CREATE USER 'admin'@'localhost' IDENTIFIED BY 'adminpw';
CREATE USER 'client'@'localhost' IDENTIFIED BY 'clientpw';

GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost';

FLUSH PRIVILEGES;

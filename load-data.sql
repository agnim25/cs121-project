LOAD DATA LOCAL INFILE 'prerequisite_courses.csv' INTO TABLE prerequisite_courses
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS;

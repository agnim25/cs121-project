-- Clean up old tables, must drop tables with foreign keys first
-- due to referential integrity constraints
DROP TABLE IF EXISTS publications;
DROP TABLE IF EXISTS keywords;
DROP TABLE IF EXISTS prerequisite_courses;
DROP TABLE IF EXISTS mentors;
DROP TABLE IF EXISTS students;

-- Represents a mentor uniquely identified by their mentor_id
CREATE TABLE mentors (
    mentor_id          INT AUTO_INCREMENT,
    mentor_name        VARCHAR(50)  NOT NULL,
    department_name    CHAR(3) NOT NULL,
    mentor_year        CHAR(2) NOT NULL,
    email              VARCHAR(50) NOT NULL,
    is_surf            BOOLEAN,
    is_academic_year   BOOLEAN,
    PRIMARY KEY (mentor_id)
);

-- Represents a publication uniquely identified by their
-- publication_id and mentor_id
CREATE TABLE publications (
    publication_id     INT AUTO_INCREMENT,
    mentor_id          INT,
    link               VARCHAR(100),
    abstract           TEXT,
    publication_date   DATE,
    PRIMARY KEY (publication_id, mentor_id),
    FOREIGN KEY (mentor_id)
        REFERENCES mentors(mentor_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Represents keywords that summarize mentor's research interests
CREATE TABLE keywords (
    keyword     VARCHAR(100),  
    mentor_id   INT,
    PRIMARY KEY (keyword, mentor_id),
    FOREIGN KEY (mentor_id)
        REFERENCES mentors(mentor_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Represents courses required in order to work with a mentor
CREATE TABLE prerequisite_courses (
    course      VARCHAR(50),
    mentor_id   INT,
    PRIMARY KEY (course, mentor_id),
    FOREIGN KEY (mentor_id)
        REFERENCES mentors(mentor_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Represents a student uniquely identified by their mentor_id
CREATE TABLE students (
    student_id     INT AUTO_INCREMENT,
    student_name   VARCHAR(50) NOT NULL,
    email          VARCHAR(50) NOT NULL,
    interests      TEXT,
    PRIMARY KEY (student_id)
)

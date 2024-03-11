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
    -- department the mentor is a part of
    department_name    VARCHAR(50) NOT NULL,
    -- year of grad student mentor (G1, G2, etc.)
    mentor_year        CHAR(2) NOT NULL,
    email              VARCHAR(50) NOT NULL,
    -- whether the mentor is taking students for surf
    is_surf            BOOLEAN,
    -- whether the mentor is taking students during academic year
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
CREATE INDEX publication_date_idx ON publications(publication_date);

-- Represents keywords that summarize mentor's research interests
CREATE TABLE keywords (
    -- mentors can enter text describing their research interests
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
    -- course number and course name (e.g. CS 155: Machine Learning)
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
    -- students can enter text describing their research interests
    interests      TEXT,
    PRIMARY KEY (student_id)
);

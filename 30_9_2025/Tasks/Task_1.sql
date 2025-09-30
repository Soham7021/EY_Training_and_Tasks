CREATE DATABASE UniversityDB;
USE UniversityDB;
-- Students Table
CREATE TABLE Students (
student_id INT PRIMARY KEY,
name VARCHAR(50),
city VARCHAR(50)
);
-- Courses Table
CREATE TABLE Courses (
course_id INT PRIMARY KEY,
course_name VARCHAR(50),
credits INT
);
-- Enrollments Table
CREATE TABLE Enrollments (
enroll_id INT PRIMARY KEY,
student_id INT,
course_id INT,
grade CHAR(2),
FOREIGN KEY (student_id) REFERENCES Students(student_id),
FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);
-- Insert Students
INSERT INTO Students VALUES
(1, 'Rahul', 'Mumbai'),
(2, 'Priya', 'Delhi'),
(3, 'Arjun', 'Bengaluru'),
(4, 'Neha', 'Hyderabad'),
(5, 'Vikram', 'Chennai');
-- Insert Courses
INSERT INTO Courses VALUES
(101, 'Mathematics', 4),
(102, 'Computer Science', 3),
(103, 'Economics', 2),
(104, 'History', 3);
-- Insert Enrollments
INSERT INTO Enrollments VALUES
(1, 1, 101, 'A'),
(2, 1, 102, 'B'),
(3, 2, 103, 'A'),
(4, 3, 101, 'C'),
(5, 4, 102, 'B'),
(6, 5, 104, 'A');


-- Level 1
-- 1
Delimiter $$
create procedure GetAllStudents()

begin
	select s.name from Students s;
end $$

Delimiter ;
call GetAllStudents();

-- 2

Delimiter $$
create procedure GetAllCourses()

begin
	select c.course_name from Courses c;
end $$

Delimiter ;
call GetAllCourses();

-- 3

Delimiter $$
create procedure GetAllStudentFromCity(in cty varchar(50))
begin
	select s.name from students s
    where s.city = cty;
end $$

Delimiter ;
call GetAllStudentFromCity("Mumbai");

-- Level 2
-- 1

Delimiter $$
create procedure GetAllStudentJoinCoursesss()
begin
	select s.name, s.student_id, c.course_id, course_name, e.student_id, e.course_id from Students s
    join Enrollments e on s.student_id = e.student_id
    join Courses c on e.course_id = c.course_id;
end $$

Delimiter ;
call GetAllStudentJoinCoursesss()

-- 2
Delimiter $$
create procedure GetAllStudentJoinCourseFromCourse(in c_i int)
begin
	select s.name from Students s
    join Enrollments e on s.student_id = e.student_id
    join Courses c on e.course_id = c.course_id
    where c.course_id = c_i;
end $$

Delimiter ;
call GetAllStudentJoinCourseFromCourse(101)

-- 3
Delimiter $$
create procedure GetAllCountStudentJoinCoursee()
begin
	select c.course_name, count(s.name) from Students s
    join Enrollments e on s.student_id = e.student_id
    join Courses c on e.course_id = c.course_id
    GROUP BY c.course_name;
end $$

Delimiter ;
call GetAllCountStudentJoinCoursee()

-- Level 3
-- 1

Delimiter $$
create procedure GetAllStudentThreeJoinCourseFromCourse()
begin
	select s.name, e.grade from Students s
    join Enrollments e on s.student_id = e.student_id
    join Courses c on e.course_id = c.course_id;
end $$

Delimiter ;
call GetAllStudentThreeJoinCourseFromCourse()

-- 2


DELIMITER $$
CREATE PROCEDURE CoursesByStudent(IN sid INT)
BEGIN
    SELECT c.course_name, e.grade
    FROM Enrollments e
    JOIN Courses c ON e.course_id = c.course_id
    WHERE e.student_id = sid;
END $$
DELIMITER ;
call CoursesByStudent(1)

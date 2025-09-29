create database School;

use School;

DROP TABLE Subject;


CREATE TABLE Subjects (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(50)
);


CREATE TABLE Teachers (
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    subject_id INT,
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id)
);


INSERT INTO Subjects (subject_name) VALUES
('Mathematics'),
('Science'),
('English'),
('History'),
('Geography');


INSERT INTO Teachers (name, subject_id) VALUES
('Rahul Sir', 1),
('Priya Madam', 2),
('Arjun Sir', NULL),
('Neha Madam', 3);

select t.name, s.subject_name
from Teachers t
inner join Subjects s 
on t.subject_id = s.subject_id;

select t.name, s.subject_name
from Teachers t
left join Subjects s 
on t.subject_id = s.subject_id;

select t.name, s.subject_name
from Teachers t
right join Subjects s 
on t.subject_id = s.subject_id;

select t.name, s.subject_name
from Teachers t
left join Subjects s 
on t.subject_id = s.subject_id
union
select t.name, s.subject_name
from Teachers t
right join Subjects s 

on t.subject_id = s.subject_id;

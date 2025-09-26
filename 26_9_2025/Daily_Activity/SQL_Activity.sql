create database SchoolDB;

Use SchoolDB;

create table Students(
  id int auto_increment primary key,
  name varchar(50),
  age int,
  course varchar(50),
  marks int
);

insert into Students(name,age,course,marks)
values
('soham','22','ai','100'),
('aniket','22','ml','50');

insert into Students(name,age,course,marks)
values
('rahul','21','ai','100'),
('balu','23','ml','50');


select * from Students;

select name, marks from students;

select * from students where marks>50;

update Students
Set marks=88, course='DS'
where id='4';

select * from Students;

Delete from Students where id='3';
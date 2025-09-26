Use SchoolDB;

create table employees(
id int auto_increment primary key,
name varchar(50) not null,
age int,
department varchar(50),
salary decimal(10,2)
);

insert into employees(name,age,department,salary)
values
('karan','22','consulting','50000.45'),
('sam','36','assurance','40000.32'),
('aniket','22','consulting','50000.56'),
('rohit','59','tax','30000.88');

select * from employees;

update employees 
set age = '23', salary='60000.78'
Where id='3';

select name, age from employees
where department = 'consulting';

select * from (select * from employees order by salary desc limit 2) as table
order by salary asc
limit 1

Delete from employees where id='2';

select * from employees;
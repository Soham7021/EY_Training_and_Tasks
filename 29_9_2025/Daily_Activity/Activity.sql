create database companydb;

use companydb;

create table Departments(
	dept_id int auto_increment primary key,
    dept_name varchar(50) not null
);

create table employess(
	emp_id int auto_increment primary key,
    name varchar(50),
    age int,
    salary decimal(10,2),
    dept_id int,
    foreign key(dept_id) references Departments(dept_id)
);

show databases;
create database RetailDB;
use RetailDB;

create table Customers(
	customer_id int auto_increment primary key,
    name varchar(50),
    city varchar(50),
    phone varchar(15)
);

create table Products(
	product_id int auto_increment primary key,
    product_name varchar(50),
    category varchar(50),
    price decimal(10,2)
);

create table Orders(
	order_id int auto_increment primary key,
    customer_id int,
    order_date Date,
    foreign key(customer_id) references Customers(customer_id)
);

create table OrderDetails(
	order_detail_id int auto_increment primary key,
    order_id int,
    product_id int,
    quantity int,
    foreign key(order_id) references Orders(order_id),
    foreign key(product_id) references Products(product_id)
);


INSERT INTO Customers (name, city, phone) VALUES
('Rahul', 'Mumbai', '9876543210'),
('Priya', 'Delhi', '9876501234'),
('Arjun', 'Bengaluru', '9876512345'),
('Neha', 'Hyderabad', '9876523456');


INSERT INTO Products (product_name, category, price) VALUES
('Laptop', 'Electronics', 60000.00),
('Smartphone', 'Electronics', 30000.00),
('Headphones', 'Accessories', 2000.00),
('Shoes', 'Fashion', 3500.00),
('T-Shirt', 'Fashion', 1200.00);


INSERT INTO Orders (customer_id, order_date) VALUES
(1, '2025-09-01'),
(2, '2025-09-02'),
(3, '2025-09-03'),
(1, '2025-09-04');


INSERT INTO OrderDetails (order_id, product_id, quantity) VALUES
(1, 1, 1),   -- Rahul bought 1 Laptop
(1, 3, 2),   -- Rahul bought 2 Headphones
(2, 2, 1),   -- Priya bought 1 Smartphone
(3, 4, 1),   -- Arjun bought 1 Shoes
(4, 5, 3);   -- Rahul bought 3 T-Shirts


DELIMITER $$
CREATE procedure GetAllProducts()
begin
	SELECT product_id, product_name, category, price
    from Products;
End $$

DELIMITER ;
CALL GetAllProducts();

DELIMITER $$
CREATE procedure GetOrdersWithCustomers()
begin
	SELECT o.order_id, o.order_date, c.name as customer_name
    from Orders o
    join Customers c
    on o.customer_id = c.customer_id;
End $$
DELIMITER ;
CALL GetOrdersWithCustomers();


DELIMITER $$
CREATE procedure GetFullOrderDetails()
begin
	SELECT o.order_id, c.name as customer_name,
    p.product_name,
    od.quantity,
    p.price,
    (od.quantity * p.price) as Total
    From Orders o
    join Customers c On o.customer_id = c.customer_id
    join OrderDetails od on o.order_id = od.order_id
    join Products p on od.product_id = p.product_id;
End $$
DELIMITER ;
CALL GetFullOrderDetails();



DELIMITER $$
CREATE procedure GetCustomerOrders(In cust_id int)
begin
	SELECT 
		o.order_id,
        o.order_date,
        p.product_name,
        od.quantity,
        p.price,
        (od.quantity * p.price) as Total
    From Orders o
    join OrderDetails od on o.order_id = od.order_id
    join Products p on od.product_id = p.product_id
    where o.cutomer_id = cust_id;
End $$
DELIMITER ;
CALL GetFullOrderDetails();




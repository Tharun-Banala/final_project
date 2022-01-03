create database restaurant;
drop database restaurant;
create table customers
(
	CustomerId int primary key auto_increment,
    CustomerName varchar(255),
    MobileNum varchar(10) unique key,
    Email varchar(255) unique key,
    Password varchar(255),
    Address varchar(255),
    Marketing varchar(50),
    Wallet float default 0.0
);

create table delivery_agents
(
	AgentId int primary key auto_increment,
    AgentName  varchar(50),
    MobileNum varchar(10) unique key,
    Email varchar(255) unique key,
    Password varchar(255),
    Wallet float,
    AgentStatus varchar(50),
    Salary float,
    NumberOfOrders int
);

create table foodCategory
(
	CategoryId int primary key auto_increment,
    CategoryName varchar(255)
);

create table menu
(
	DishID int primary key auto_increment,
    DishName varchar(255),
    CategoryId int,
    Price float,
    Veg_NonVeg varchar(1),
    Description char,
    foreign key (CategoryId) references foodCategory(CategoryId) on delete cascade
);
alter table menu drop Description;
-- alter table menu drop active;
alter table menu add Description varchar(500);
alter table menu add column active bool default true;

create table orderDetails
(
	DetailsId int auto_increment,
    DishId int,
    Quantity int,
    primary key (DetailsId, DishId),
    foreign key (DishId) references menu(DishId) on delete cascade 
);

create table orders
(
	OrderID int primary key auto_increment,
    Date date,
    Time time,
    CustomerID int,
    DetailsId int,
    BillAmount int,
    foreign key (DetailsId) references orderDetails(DetailsId) on delete cascade,
    foreign key (CustomerId) references customers(CustomerId) on delete cascade
);


create table deliveries
(
	AgentId int,
    OrderID int,
    DeliveryStatus varchar(50),
    DeliveredTime time,
    PaymentStatus varchar(50),
    primary key(AgentId,OrderId),
    foreign key (AgentId) references delivery_agents(AgentId) on delete cascade,
    foreign key (OrderID) references orders(OrderId) on delete cascade
);

create table cart
(
	CustomerId int,
    DishId int,
    Quantity int,
    primary key (CustomerId, DishId),
    foreign key (DishId) references menu(DishId) on delete cascade,
    foreign key (CustomerId) references customers(CustomerId) on delete cascade
);

create table timeslots
(
	Slot varchar(9) primary key
);

create table tables
(
	TableId int primary key auto_increment,
    Capacity int
);

create table Reservations
(
	ReservationId int not null auto_increment unique key,
	TableId int,
    Slot varchar(9),
    Date date,
    suggestions varchar(1000),
    foreign key (TableId) references tables(TableId),
    foreign key (Slot) references timeslots(Slot),
    primary key (Date,Slot,TableId)
);

create table employee(
	employeeID int not null auto_increment,
    employeename varchar(30),
    address varchar(150),
    phonenumber varchar(13),
    workslot int,
    primary key (employeeID)
);
create table restaurant
(	
	RestaurantWallet float 
);
alter table employee add column password varchar(15) not null;
alter table employee add Designation varchar(20);
alter table employee add emailid varchar(50);
alter table employee modify workslot varchar(15);


update menu set active=0 where DishID=1;
update menu set Description="Excellent Food,Source:Trust me Bro!!";
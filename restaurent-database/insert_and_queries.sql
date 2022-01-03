insert into 
foodCategory (CategoryName) values
('Soups'),
('Appetisers'),
('Pizza and Pasta'),
('Burgers and Sandwiches'),
('Main Course'),
('Breads'),
('Rice and Biryani'),
('Desserts'),
('Beverages');

insert into 
menu (DishName, CategoryId, Price, Veg_NonVeg) values
('Veg Manchurian',2,150,'V'),
('Veg Spring Roll',2,160,'V'),
('Panner - 65',2,180,'V'),
('Chilli Baby Corn',2,160,'V'),
('Chicken Wings with Hot Sauce',2,200,'N'),
('Schezwan Manchurian',2,160,'V'),
('Chilli Mushroom',2,170,'V'),
('Crispy Corn Paper',2,170,'V'),
('Chicken Drumsticks',2,200,'N'),
('Chicken Tikka',2,180,'N'),
('Veg Schezwan Noodles',2,120,'V'),
('Chicken Noodles',2,150,'N');

insert into 
menu (DishName, CategoryId, Price, Veg_NonVeg) values
('Malai Kofta',5,200,'V'),
('Paneer Butter Masala',5,180,'V'),
('Matar Paneer',5,180,'V'),
('Dal Makhani',5,150,'V'),
('Chilli Butter Chicken',5,220,'N'),
('Shahi Chicken',5,240,'N'),
('Kadhai Mutton',5,230,'N');

insert into 
menu (DishName, CategoryId, Price, Veg_NonVeg) values
('Cheese Garlic Bread',3,120,'V'),
('Margherita Pizza',3,160,'V'),
('The Veggie Burst Pizza',3,185,'V'),
('Spiced Paneer and Bell Pepper Pizza',3,195,'V'),
('BBQ Chicken and Chilli Pizza',3,200,'N'),
('Veg Alfredo Pasta',3,190,'V'),
('Spaghetti with Meatball',3,220,'N'),
('Veg Mac and Cheese Baked Pasta',3,200,'V'),
('Veg Mushroom and Cheese Pasta',3,210,'V'),
('Non Veg Alfredo Pasta',3,210,'N');

insert into 
menu (DishName, CategoryId, Price, Veg_NonVeg) values
('Butter Naan',6,30,'V'),
('Garlic Naan',6,30,'V'),
('Rumali Roti',6,30,'V'),
('Tandoori Roti',6,40,'V');

insert into 
menu (DishName, CategoryId, Price, Veg_NonVeg) values
('Lemon Baked Cheese Cake',8,110,'N'),
('Ferrero Brownie',8,100,'N'),
('Red Velvet Cup Cake',8,80,'N'),
('Cinnamon Sugar Doughnut',8,80,'N'),
('Gulab Jamun',8,60,'V'),
('Double Ka Meetha',8,60,'V');

insert into 
menu (DishName, CategoryId, Price, Veg_NonVeg) values
('Royal Chicken Biryani',7,230,'N'),
('Royal Mutton Biryani',7,260,'N'),
('Egg Biryani',7,200,'N'),
('Veg Biryani',7,200,'V');

insert into 
menu (DishName, CategoryId, Price, Veg_NonVeg) values
('Virgin Mojito Mocktail',9,80,'V'),
('Blue Curacao Mojito',9,80,'V'),
('Fresh Lime Soda Mojito',9,80,'V'),
('Cranberry Mojito',9,80,'V'),
('Choco Oreo Shake',9,100,'V'),
('Vanilla Berry Shake',9,100,'V'),
('Brownie Shake',9,100,'N');

insert into 
menu (DishName, CategoryId, Price, Veg_NonVeg) values
('Vegetable Patty and Cheese Burger',4,150,'V'),
('Spicy Paneer Grilled Burger',4,175,'V'),
('BBQ Chicken and Cheese Grilled Burger',4,200,'N'),
('Whopper Chicken Burger',4,180,'N'),
('Spinach and Corn Toast Sandwich',4,100,'V'),
('Vegetable Grilled Sandwich',4,110,'V'),
('Chicken Keema and Cheese Sandwich',4,120,'N');

insert into 
menu (DishName, CategoryId, Price, Veg_NonVeg) values
('Tomato Soup',1,100,'V'),
('Babycorn Soup',1,100,'V'),
('Mushroom Soup',1,120,'V'),
('Hot and Sour Soup',1,100,'V'),
('Chicken Manchow Soup',1,120,'N'),
('Noodles Soup',1,120,'V'),
('Chicken Sweetcorn Soup',1,120,'N');

insert into 
timeslots (Slot) values
('12pm-1pm'),
('1pm-2pm'),
('2pm-3pm'),
('3pm-4pm'),
('4pm-5pm'),
('5pm-6pm'),
('6pm-7pm'),
('7pm-8pm'),
('8pm-9pm'),
('9pm-10pm'),
('10pm-11pm'),
('11pm-12am');

insert into tables (Capacity) values
(2),
(2),
(2),
(4),
(4),
(4),
(4),
(6),
(6),
(8);

insert into 
delivery_agents (AgentName,MobileNum,Email,Password,Wallet,AgentStatus,Salary,NumberOfOrders) values
('Mahesh Babu','9959782483','sahasreddy1707@gmail.com','1',0.0,'Available',20000,0),
('Ramesh','9959782723','iampeterbtw@gmail.com','2',0.0,'Available',20000,0),
('Shahrukh','9959896366','karthikboddupalli888@gmail.com','3',0.0,'Available',20000,0);

update delivery_agents set AgentStatus='Available' where AgentId=1;
update delivery_agents set Email='mahesh1@gmail.com' where AgentId=1;
update delivery_agents set Email='ramesh2@gmail.com' where AgentId=2;
update delivery_agents set Email='shahrukh3@gmail.com' where AgentId=3;

select * from delivery_agents;

select * from customers;

insert into employee values (1,'Raj','Address','9133208090','Morning','12345','admin','karthikboddupalli888@gmail.com');

insert into 
restaurant(RestaurantWallet)
values (0);
select * from restaurant;
update restaurant set RestaurantWallet = 100000;

update customers set wallet=1200 where CustomerId=2;

select * from employee;

update employee set employeename='Sahas Reddy',
emailid='sahasreddy1707@gmail.com',
address='H.No. 10-25-4, N.S.Nagar, Markapur',
phonenumber='9959782483' where employeeID=1;
from flask import Flask, render_template, request, redirect, session, jsonify
from flask.helpers import make_response
import random
import smtplib
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(10)
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="tharun@159",
  database="restaurant",
)
mycursor=mydb.cursor()

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/adminlogin')
def adminlogin():
  return render_template('adminlogin.html')
  
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')

Email=''
@app.route('/login_validation', methods=['POST'])
def login_validation():
    admin=request.form.get('Administrator')
    if not admin:
      global Email
      Email = request.form.get('Email')
      password = request.form.get('password')
      mycursor.execute('SELECT * FROM customers WHERE Email=%s AND Password=%s',(Email,password))
      customers = mycursor.fetchall()
      if len(customers)>0:
          session['CustomerId'] = customers[0][0]
          session['Customername']=customers[0][1]
          return redirect('/')
      else:
          return render_template('login.html', error_message="Invalid Email Id or Password")
    else:
      Email = request.form.get('Email')
      password = request.form.get('password')
      mycursor.execute('SELECT * FROM employee WHERE emailid=%s AND password=%s',(Email,password))
      emps = mycursor.fetchall()
      if len(emps)>0:
          session['CustomerId'] = emps[0][0]
          session['Customername']=emps[0][1]
          session['admin']=True
          return redirect('/')
      else:
          return render_template('login.html', error_message="Invalid Email Id or Password")

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/addemployee')
def addemployee():
  return render_template('addemployee.html')

    
@app.route('/menu')
def menu():
  mycursor.execute("""select * from foodCategory""")
  foodCategories = mycursor.fetchall()
  mycursor.execute("""select * from menu""")
  menu = mycursor.fetchall()
  print(menu)
  
    
  return render_template('menu.html', foodCategories=foodCategories, menu=menu)

@app.route('/menuchange',methods=['POST','GET'])
def menchange():
  mycursor.execute("""select max(`DIshID`) from `menu`""")
  m=mycursor.fetchall()
  mx=m[0][0]+1
  mycursor.execute('select * from foodCategory')
  cat=mycursor.fetchall()
  rem=request.form.get('removeit')
  add=request.form.get('AddIt')
  chit=request.form.get('changeit')
  adon=request.form.get('adon')
  if adon!=None:
    return render_template('change.html',dish=None,mx=mx,cat=cat)
  elif rem!=None:
    mycursor.execute("""update `menu` set `active`=0 where DishID='{}'""".format(int(rem)))
    mydb.commit()
    return redirect('/menu')
  elif add!=None:
    mycursor.execute("""update `menu` set `active`=1 where DishID='{}'""".format(int(add)))
    mydb.commit()
    return redirect('/menu')
  elif chit!=None:
    # print(chit)
    mycursor.execute("""select * from `menu` where `DishID`='{}'""".format(int(chit)))
    k=mycursor.fetchall()
    dish=k[0] 
    print(dish)
    return render_template('change.html',dish=dish,mx=mx,cat=cat)
  else:
    return redirect('/menu')

@app.route('/changeconts',methods=["POST","GET"])
def changeconts():
  dishId=request.form.get("dishid")
  file = request.files['image']
  if file:
    filename=str(dishId+".png")
    fileloc='static/img/menu/'
    print(filename)
    file.save(os.path.join(fileloc, filename))
  vn=request.form.get('vn')
  title=request.form.get('title')
  price=request.form.get('price')
  description=request.form.get('description')
  CategoryId=request.form.get('CategoryId')
  mycursor.execute('select max(DIshID) from menu')
  m=mycursor.fetchall()
  mx=m[0][0]+1
  if not (int(dishId)==mx) :
    mycursor.execute("""update `menu` set `DishName`='{}' , `CategoryId`='{}' , `Price`='{}' , `Veg_NonVeg`='{}' , `Description`='{}' where `DishID`='{}'""".format(title,CategoryId,price,vn,description,dishId))
    mydb.commit()
  else:
    mycursor.execute("""insert into `menu`(`DishID`,`DishName`,`CategoryId`,`Price`,`Veg_NonVeg`,`Description`,`active`) value('{}','{}','{}','{}','{}','{}',1)""".format(dishId,title,CategoryId,price,vn,description))
    mydb.commit()
  return redirect('/menu')


@app.route('/admininfo')
def admininfo():
  mycursor.execute("""select * from employee where employeeID='{}'""".format(session['CustomerId']))
  empinfodframe=mycursor.fetchall()
  empinfo=empinfodframe[0]
  mycursor.execute("""select * from `Reservations` where `Date`>(Select CURRENT_DATE()) order by `Date` asc""")
  reservations=mycursor.fetchall()

  mycursor.execute("""select `RestaurantWallet` from `Restaurant`""")
  RestaurantWallet=mycursor.fetchall()
  RestaurantWallet=RestaurantWallet[0][0]

  mycursor.execute("""select * from `orders` order by `OrderId` desc""")
  orderstaken = mycursor.fetchall()
  orderdetails={}
  delivery_info={}
  delivery_agent_info={}
  for i in orderstaken:
    mycursor.execute("""select `menu`.`DishName`,`orderDetails`.`Quantity`,(`menu`.`Price`)*(`orderDetails`.`Quantity`) from (`orderDetails` inner join `menu` on `orderDetails`.`DishId`=`menu`.`DishID` )  where  `orderDetails`.`DetailsId`= '{}'""".format(i[4]))
    orderdetails[i[4]]=mycursor.fetchall()

    mycursor.execute("""select * from deliveries where OrderId='{}'""".format(i[0]))
    delivery_info[i[0]] = mycursor.fetchall()

    mycursor.execute("""select `AgentName`, `MobileNum` from `delivery_agents` where `AgentId`='{}'""".format(delivery_info[i[0]][0][0]))
    delivery_agent_info[i[0]] = mycursor.fetchall()

  return render_template('admininfo.html', empinfo=empinfo,reservations=reservations, orderstaken=orderstaken,orderdetails=orderdetails, delivery_info=delivery_info, delivery_agent_info=delivery_agent_info, RestaurantWallet=RestaurantWallet)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
  if 'CustomerId' in session:
    print(session['CustomerId'])
    addDishId = request.form.get('addDishId')
    mycursor.execute("""insert into `cart` (`CustomerId`, `DishId`, `Quantity`) values ('{}', '{}', '{}')""".format(session['CustomerId'], addDishId, 1))
    mydb.commit()
    return redirect('/menu')
  else:
    return render_template('login.html', message='First, you should login. Then you can add food to your cart')

@app.route('/cart')
def cart():
  if 'CustomerId' in session:
    mycursor.execute("""select Address from customers where CustomerId='{}'""".format(session['CustomerId']))
    myAddress = mycursor.fetchall()
    print(myAddress)
    mycursor.execute("""select menu.DishName, menu.Price, cart.Quantity, menu.DishId from (cart inner join menu) where cart.CustomerId='{}' and cart.DishId=menu.DishId""".format(session['CustomerId']))
    cartDishes = mycursor.fetchall()
    emptyCart = False
    if (cartDishes==[]):
      emptyCart = True
    subTotalBill = 0
    for dish in cartDishes:
      subTotalBill += dish[1]*dish[2]
    
    return render_template('cart.html', emptyCart=emptyCart, cartDishes=cartDishes, subTotalBill=subTotalBill, totalBill = subTotalBill+30, myAddress=myAddress[0][0])
  else:
    return render_template('login.html', message='First, you should login. Then you get your cart')


payment_otp = 0

payment_method = ''

@app.route('/place_order', methods=['GET','POST'])
def place_order():
  dish_id_delete = request.form.get("remove_itemid")
  changeAddress = request.form.get("changeAddress")
  makePayment = request.form.get("makePayment")
  global payment_method
  payment_method = request.form.get("payment_method")

  if payment_method != None:

    if payment_method == "no_option":
      return render_template("payment.html", error_message="Select a valid payment method")
    elif payment_method == "cod":
      return redirect('/place_order_continued')
    elif payment_method == "ewallet":
      mycursor.execute("""select menu.DishId, menu.Price, cart.Quantity, menu.DishName from (cart inner join menu) where cart.CustomerId='{}' and cart.DishId=menu.DishId""".format(session['CustomerId']))
      cartDishes = mycursor.fetchall()
      # print(cartDishes)
      totalBill = 30
      for dish in cartDishes:
        totalBill += dish[1]*dish[2]
        
      mycursor.execute("""select Wallet,Email from customers where CustomerId='{}'""".format(session['CustomerId']))
      balance = mycursor.fetchall()
      if balance[0][0]>=totalBill:

        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.starttls()

        s.login("restaurants1233@gmail.com", "restrest")
        global payment_otp
        payment_otp=random.randint(10000,99999)

        message = "Your OTP for the payment of INR {} from your E-Wallet".format(totalBill) + " is "+str(payment_otp)

        s.sendmail("restuarants1233@gmail.com",balance[0][1], message)

        s.quit()

        return render_template('wallet.html', totalBill=totalBill, balance=balance[0][0])

      else:
        return render_template('payment.html', error_message="Insufficient balance in your E-Wallet", balance_message="Balance: INR {}".format(balance[0][0]), bill_message="Total Bill: INR {}".format(totalBill))

  elif dish_id_delete != None:
    print(dish_id_delete)
    mycursor.execute("""delete from `cart` where `CustomerId`='{}' and `DishId`='{}'""".format(session['CustomerId'],dish_id_delete))
    mydb.commit()
    return redirect("/cart")

  elif changeAddress != None:
    return redirect("/update_profile")

  elif makePayment != None:
    mycursor.execute("""select menu.DishId, menu.Price, cart.Quantity, menu.DishName from (cart inner join menu) where cart.CustomerId='{}' and cart.DishId=menu.DishId""".format(session['CustomerId']))
    cartDishes = mycursor.fetchall()
      # print(cartDishes)
    for dish in cartDishes:
      dish_quantity = request.form.get(dish[3])
      print(dish_quantity)
      mycursor.execute("""update `cart` set `Quantity` = '{}' where `DishId` = '{}'""".format(dish_quantity, dish[0]))
      mydb.commit()
     
    
    mycursor.execute("""select * from delivery_agents where AgentStatus='Available'""")
    availableAgents = mycursor.fetchall()
    print(availableAgents)
    if len(availableAgents) == 0:
      return render_template('orderFinished.html', message="Sorry, all of our delivery agents are busy right now...Please try again after some time", message_code="Agents_Unavailable")
    else:
      return render_template('payment.html')
    

@app.route('/payment_otp_authentication', methods=["POST", "GET"])
def payment_otp_authentication():
  entered_otp=request.form.get('entered_otp')
  entered_otp=int(entered_otp)
  if entered_otp != payment_otp : 
    error_message="Invalid OTP - Payment failed. Please try again!"
    return render_template('payment.html',error_message=error_message)
  else:
    mycursor.execute("""select menu.DishId, menu.Price, cart.Quantity, menu.DishName from (cart inner join menu) where cart.CustomerId='{}' and cart.DishId=menu.DishId""".format(session['CustomerId']))
    cartDishes = mycursor.fetchall()
    totalBill = 30
    for dish in cartDishes:
      totalBill += dish[1]*dish[2]

    mycursor.execute("""update customers set Wallet = Wallet - {} where CustomerId='{}'""".format(totalBill, session['CustomerId']))
    mydb.commit()

    mycursor.execute("""update restaurant set RestaurantWallet = RestaurantWallet + {}""".format(totalBill))
    mydb.commit()
    return redirect('/place_order_continued')


@app.route('/place_order_continued', methods=["POST", "GET"])
def place_order_continued():
  
  #adding data into orderDetails
  mycursor.execute("""select max(DetailsId) from orderDetails""")
  maxDetailsIdList = mycursor.fetchall()
  maxDetailsId = maxDetailsIdList[0][0]
  if maxDetailsId==None:
    addDetailsId = 1
  else:
    addDetailsId = maxDetailsId + 1
  # print(maxDetailsId)
  # print(addDetailsId)
  mycursor.execute("""select menu.DishId, menu.Price, cart.Quantity, menu.DishName from (cart inner join menu) where cart.CustomerId='{}' and cart.DishId=menu.DishId""".format(session['CustomerId']))
  cartDishes = mycursor.fetchall()
  # print(cartDishes)
  totalBill = 30
  for dish in cartDishes:
    mycursor.execute("""insert into `orderDetails` (`DetailsId`, `DishId`, `Quantity`) values ('{}', '{}', '{}')""".format(addDetailsId, dish[0], dish[2]))
    mydb.commit()
    totalBill += dish[1]*dish[2]

  #adding data into orders
  mycursor.execute("""select CURRENT_TIME""")
  time = mycursor.fetchall()
  TIME = time[0][0]
  mycursor.execute("""select CURRENT_DATE""")
  date = mycursor.fetchall()
  DATE = date[0][0]
  # print(addDateTime)
  # print(type(addDateTime))
  mycursor.execute("""insert into `orders` (`Date`,`Time`, `CustomerId`, `DetailsId`, `BillAmount`) values ('{}','{}', '{}', '{}', '{}')""".format(DATE,TIME , session['CustomerId'], addDetailsId, totalBill))
  mydb.commit()

  #deleting from cart
  mycursor.execute("""delete from `cart` where `CustomerId`='{}'""".format(session['CustomerId']))
  mydb.commit()

  #getting orderId
  mycursor.execute("""select max(OrderId) from orders""")
  orderId = mycursor.fetchall()
  orderId = orderId[0][0]

  #assigning deliver agent to this order
  mycursor.execute("""select * from delivery_agents where AgentStatus='Available'""")
  availableAgents = mycursor.fetchall()
  print(availableAgents)
  minOrders = 100000
  for agent in availableAgents:
    if agent[8] < minOrders:
      minOrders = agent[8]
  mycursor.execute("""select * from delivery_agents where AgentStatus='Available' and NumberOfOrders='{}'""".format(minOrders))
  minOrderAgents = mycursor.fetchall()
  assignedAgent = minOrderAgents[0]

  #changing status of delivery agent
  mycursor.execute("""update delivery_agents set AgentStatus='NotAvailable', NumberOfOrders = NumberOfOrders+1 where AgentId='{}'""".format(assignedAgent[0]))
  mydb.commit()
  
  payment_status = ''
  if payment_method=='cod':
    payment_status = 'Cash-On-Delivery'
  elif payment_method=='ewallet':
    payment_status = 'Paid'
  
  mycursor.execute("""insert into `deliveries` (`AgentId`, `OrderId`, `DeliveryStatus`, `PaymentStatus`) values ('{}', '{}', 'Preparing', '{}')""".format(assignedAgent[0], orderId, payment_status))
  mydb.commit()


  return render_template('orderFinished.html', message="Hurray!! The order has been placed, your delicious food is enroute",message_code="Successful")


@app.route('/myorders',methods=["POST","GET"])
def myorders():
  # print("hello")
  if 'CustomerId' in session:
    mycursor.execute("""select * from `orders` where  `CustomerId`= '{}' order by `OrderId` desc""".format(session['CustomerId']))
    orderstaken = mycursor.fetchall()
    orderdetails={}
    delivery_info={}
    delivery_agent_info={}
    # statusreport={}
    for i in orderstaken:
      mycursor.execute("""select `menu`.`DishName`,`orderDetails`.`Quantity`,(`menu`.`Price`)*(`orderDetails`.`Quantity`) from (`orderDetails` inner join `menu` on `orderDetails`.`DishId`=`menu`.`DishID` )  where  `orderDetails`.`DetailsId`= '{}'""".format(i[4]))
      orderdetails[i[4]]=mycursor.fetchall()

      mycursor.execute("""select * from deliveries where OrderId='{}'""".format(i[0]))
      delivery_info[i[0]] = mycursor.fetchall()

      mycursor.execute("""select `AgentName`, `MobileNum` from `delivery_agents` where `AgentId`='{}'""".format(delivery_info[i[0]][0][0]))
      delivery_agent_info[i[0]] = mycursor.fetchall()

    return render_template('myOrders.html', orderstaken=orderstaken,orderdetails=orderdetails, delivery_info=delivery_info, delivery_agent_info=delivery_agent_info)
      # mycursor.execute("""select * from `Delivery`  where  `orderID`= '{}'""".format(i[0]))
      # deliverydetails=mycursor.fetchall()
      # statusreport[i[0]]=deliverydetails[0][3]
    # Noorder = False
    # if (orderstaken==[]):
      # Noorder = True
      
    # return render_template('myOrders.html', orderstaken=orderstaken,orderdetails=orderdetails,statusreport=statusreport,deliverydetails=deliverydetails)
  else:
    return render_template('login.html', message='First, you should login. Then you can see your Orders')


@app.route('/reservations')
def reservations():
  if 'CustomerId' in session:
    mycursor.execute("""SELECT DATE_ADD( CURRENT_DATE(), interval 1 day)""")
    tomdate=mycursor.fetchall()
    mycursor.execute("""select distinct Capacity from tables""")
    capacities = mycursor.fetchall()
    # print(capacities)
    return render_template ('reservations.html', capacities=capacities, slot_table={},tomdate=tomdate)
  else:
    return render_template('login.html', message='First, you should login. Then you can reserve a table')


@app.route('/check_availability', methods=['GET','POST'])
def check():
  capacity = request.form.get('capacity')
  print(capacity)
  date=request.form.get('date')
  global select_date
  select_date=date
  mycursor.execute("""select tables.TableId, timeslots.Slot from (tables cross join timeslots) 
  where tables.TableId not in (select TableId from Reservations where Slot = timeslots.Slot and Date='{}') and tables.Capacity='{}' ;""".format(date,capacity))
  availability = mycursor.fetchall()
  print(availability)
  mycursor.execute("""SELECT DATE_ADD( CURRENT_DATE(), interval 1 day)""")
  tomdate=mycursor.fetchall()
  slot_table = {}
  for pair in availability:
    slot_table[pair[1]] = pair[0]
  return render_template('reservations.html', slot_table=slot_table,tomdate=tomdate)


@app.route('/make_reservation', methods=['POST', 'GET'])
def make_reservation():
  reservedSlotTable = request.form.get('slotTable')
  suggesition=request.form.get('suggesitions')
  # print(reservedSlotTable)
  [reservedSlot, reservedTable] = reservedSlotTable.split('+')
  global select_date
  mycursor.execute("""insert into `Reservations` (`TableId`,`Date` ,`Slot`,`suggestions`) values ('{}','{}','{}','{}')""".format(reservedTable,select_date,reservedSlot,suggesition))
  mydb.commit()
  mycursor.execute("""select `ReservationId` from Reservations where TableId='{}'and Date='{}'and Slot='{}'""".format(reservedTable,select_date,reservedSlot))
  reservationid=mycursor.fetchall()
  mycursor.execute("""SELECT DATE_ADD( CURRENT_DATE(), interval 1 day)""")
  tomdate=mycursor.fetchall()
  return render_template('reservations.html',tomdate=tomdate, message=" Table {} will be reserved for you at {} on {}. Your Regeservation ID is {} .".format(reservedTable, reservedSlot,select_date,reservationid[0][0]), slot_table={})

addName=''
addMobileNum=''
addEmail=''
addPassword=''
addAddress=''
addMarketing=''
addworkslot=''
addaddress=''
designation=''
emp=None
n=0
@app.route('/add_user', methods=['POST'])
def add_user():
    global emp
    emp=request.form.get('admin')
    global addName
    addName= request.form.get('reg_name')
    global addMobileNum 
    addMobileNum = request.form.get('reg_MobileNum')
    global addEmail
    addEmail= request.form.get('reg_Email')
    global addPassword 
    addPassword= request.form.get('reg_Password')
    global addAddress
    addAddress = request.form.get('reg_Address')
    global addMarketing
    addMarketing = request.form.get('marketing')
    global addworkslot 
    addworkslot= request.form.get('workslot')
    global addaddress 
    addaddress= request.form.get('address')
    global designation
    designation=request.form.get('designation')
    print(addPassword)
    print(addEmail)

    if len(addMobileNum)!=10 or (not addMobileNum.isdigit()) :
      if emp is not None:
        return render_template('addemployee.html', error_message='Enter a valid mobile number')
      else:
        return render_template('register.html', error_message='Enter a valid mobile number')
    if emp is not None:
      mycursor.execute ("""SELECT * FROM employee WHERE emailid='{}'""".format(addEmail))
      customers = mycursor.fetchall()
      if len(customers)>0:
          return render_template('addemployee.html', message='Entered Email address was already registered. Login to proceed')
    else:
      mycursor.execute ("""SELECT * FROM customers WHERE Email='{}'""".format(addEmail))
      customers = mycursor.fetchall()
      if len(customers)>0:
          return render_template('register.html', message='Entered Email address was already registered. Login to proceed')
    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login("restaurants1233@gmail.com", "restrest")
    global n
    n=random.randint(10000,99999)

    message = "Your OTP is "+str(n)

    s.sendmail("restuarants1233@gmail.com",addEmail, message)
    print(n)
    s.quit()
    return render_template('otp.html')

@app.route('/otp_authentication', methods=['POST'])
def otp1():
     x=request.form.get('otp')
     print(x)
     print(n)
     y=int(x)
     global addPassword,addEmail,addName,addPassword
     if y!=n :
         error_message="Invalid OTP"
         return render_template('otp.html',error_message=error_message)
    
    
     if emp is not None:
       mycursor.execute("""insert into `employee` (`employeename`, `phonenumber`, `emailid`, `password`,`address`,`workslot`,`Designation`) values('{}', '{}', '{}', '{}','{}','{}','{}')""".format(addName, addMobileNum, addEmail, addPassword,addaddress,addworkslot,designation))
       mydb.commit()
       return render_template('login.html', after_reg_message="Account created successfully! Login to proceed")
     else:
        mycursor.execute("""insert into `customers` (`CustomerName`, `MobileNum`, `Email`, `Password`, `Address`, `Marketing`) values('{}', '{}', '{}', '{}', '{}', '{}')""".format(addName, addMobileNum, addEmail, addPassword, addAddress, addMarketing))
        mydb.commit()
        return render_template('login.html', after_reg_message="Account created successfully! Login to proceed")
        
@app.route('/userhomepage')
def profile():
  mycursor.execute("""select * from `customers`  where  `CustomerId`= '{}'""".format(session['CustomerId']))
  userdetails=mycursor.fetchall()
  print(userdetails)
  mycursor.execute("""select count(OrderID), sum(BillAmount) from `orders`  where  `CustomerId`= '{}'""".format(session['CustomerId']))
  details=mycursor.fetchall()
  print(details)
  return render_template('profile.html',userdetails=userdetails,details=details)

@app.route('/delivery_agent_login', methods=['GET', 'POST'])
def delivery_agent_login():
  return render_template('delivery_agent_login.html')


@app.route('/delivery_agent_login_validation', methods=['GET', 'POST'])
def delivery_agent_login_validation():
  Email = request.form.get('Email')
  password = request.form.get('password')
  mycursor.execute('SELECT * FROM delivery_agents WHERE Email=%s AND Password=%s',(Email,password))
  agents = mycursor.fetchall()
  if len(agents)>0:
      session['AgentId'] = agents[0][0]
      return redirect('/deliveries')
  else:
      return render_template('delivery_agent_login.html', error_message="Invalid Email Id or Password")

@app.route('/deliveries', methods=['GET', 'POST'])
def deliveries():
  
  mycursor.execute("""select * from deliveries where AgentId = '{}' order by `OrderId` desc""".format(session['AgentId']))
  deliveries = mycursor.fetchall()
  orderdetails={}
  customer_info={}
  assignedOrders={}
  currentOrder=False

  for delivery in deliveries:
    if delivery[2]!="Delivered":
      currentOrder=True
    mycursor.execute("""select * from `orders`  where  `OrderId`= '{}'""".format(delivery[1]))
    order = mycursor.fetchall()
    assignedOrders[delivery[1]] = order[0]

    detailsId = order[0][4]
    customerId = order[0][3]

    mycursor.execute("""select `menu`.`DishName`,`orderDetails`.`Quantity`,(`menu`.`Price`)*(`orderDetails`.`Quantity`) from (`orderDetails` inner join `menu` on `orderDetails`.`DishId`=`menu`.`DishID` )  where  `orderDetails`.`DetailsId`= '{}'""".format(detailsId))

    ODetails = mycursor.fetchall()
    orderdetails[delivery[1]] = ODetails

    mycursor.execute("""select `CustomerName`, `MobileNum`, `Address` from `customers` where `CustomerId` = '{}'""".format(customerId))
    CInfo = mycursor.fetchall()
    customer_info[delivery[1]] = CInfo[0]


  return render_template('delivery.html', currentOrder=currentOrder, deliveries=deliveries, assignedOrders=assignedOrders, orderdetails=orderdetails, customer_info=customer_info)

@app.route('/order_status_change', methods=['GET', 'POST'])
def order_status_change():
  preparing_to_enroute = request.form.get("preparing_to_enroute")
  enroute_to_delivered = request.form.get("enroute_to_delivered")

  if preparing_to_enroute != None and (enroute_to_delivered==None):
    mycursor.execute("""update `deliveries` set `DeliveryStatus` = "Enroute" where `OrderId` = '{}'""".format(preparing_to_enroute))
    mydb.commit()
  elif enroute_to_delivered != None and (preparing_to_enroute == None):
    mycursor.execute("""select CURRENT_TIME""")
    time = mycursor.fetchall()
    TIME = time[0][0]
    mycursor.execute("""update `deliveries` set `DeliveryStatus` = "Delivered", `PaymentStatus` = "Paid", `DeliveredTime` = '{}' where `OrderId` = '{}'""".format(TIME, enroute_to_delivered))
    mydb.commit()

    mycursor.execute("""update `delivery_agents` set `AgentStatus` = "Available" where AgentId = '{}'""".format(session['AgentId']))
    mydb.commit()

  return redirect('/deliveries')

@app.route('/customersInfo', methods=['GET', 'POST'])
def customersInfo():
  mycursor.execute("""select `CustomerId`, `CustomerName`, `Email`, `MobileNum`, `Wallet` from `Customers`""")
  customers = mycursor.fetchall()
  return render_template('customers_info.html', customers=customers)

@app.route('/update_customer_wallet', methods=['GET', 'POST'])
def update_customer_wallet():
  CustomerId = request.form.get("CustomerId")
  Amount = request.form.get("Amount")
  mycursor.execute("""update `customers` set Wallet = Wallet + {} where CustomerId = '{}'""".format(Amount, CustomerId))
  mydb.commit()
  return redirect('/customersInfo')

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
  mycursor.execute("""select * from `customers`  where  `CustomerId`= '{}'""".format(session['CustomerId']))
  userdetails=mycursor.fetchall()
  print(userdetails)
  return render_template("update_profile.html", userdetails=userdetails)

@app.route('/update_profile_database', methods=['GET', 'POST'])
def update_profile_database():
  newAddress = request.form.get('Address')
  print(newAddress)
  if newAddress != "":
    mycursor.execute("""update `customers` set `Address` = '{}' where `CustomerId` = '{}'""".format(newAddress, session['CustomerId']))
    mydb.commit()

  return redirect('/userhomepage')



if __name__ == '__main__':
  app.run(debug=True)

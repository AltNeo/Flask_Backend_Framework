create database Dummy;
use Dummy;

create database Application;
/* Need to enable encyption on the field pwd*/
create table Login(
    mail varchar(40) NOT NULL, 
    adminID int auto_increment UNIQUE KEY, 
    pwd varchar(48) NOT NULL,
    username varchar(20) PRIMARY KEY NOT NULL,
);

###NOT RUN YET###
CREATE TABLE LoginHistory (
    login_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES Login(username)
);
/*
//enquiry?? for customer?
//orderHistory will be a foreign key
*/
create table Customer(
    customer_id int auto_increment NOT NULL PRIMARY KEY,
    name varchar(30) NOT NULL,
    mail varchar(40) NOT NULL,
    phone varchar(12) NOT NULL UNIQUE,
    address varchar(100) NOT NULL,
    cart_item varchar(200) NOT NULL,
    joindate date NOT NULL,
    enquiry varchar(200) NOT NULL,
    orderHistory varchar(200),
    otp varchar(4)
    /*Order History will be changed adding orderID every time a new order is added*/
    /*Foreign key orderHistory*/
);



create table Category(
    category_name varchar(20) NOT NULL,
    category_id int auto_increment NOT NULL PRIMARY KEY,
    category_Image varchar(200) NOT NULL
);

create table Product(
    name varchar(20) NOT NULL,
    price int NOT NULL,
    descr varchar(200) NOT NULL,
    product_id int auto_increment NOT NULL PRIMARY KEY,
    stock varchar(200) NOT NULL,
    category_id int NOT NULL,
    estimated_price varchar(200) NOT NULL,
    /*#####image varchar(200) NOT NULL,*/
    GSM int,
    material varchar(200) NOT NULL,
    margin int NOT NULL,
    displaystate BINARY NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Category(category_id)
    /*Foreign Key category_id */
);
///
ALTER TABLE Product ADD COLUMN color VARCHAR(255) NOT NULL;
ALTER TABLE Product ADD COLUMN images TEXT;
///


###
YET YO RUN
###
Create table OrderHistory(
    order_id varchar(300) NOT NULL PRIMARY KEY,
    customer_id int,
    
)


####
YET TO RUN
####
CREATE TABLE ProductImage (
    product_image_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    product_id INT NOT NULL,
    image_link VARCHAR(200) NOT NULL,
    color VARCHAR(20),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

###
Yet to run
###
CREATE TABLE `dummy`.`adminlogin` (
  `admin_id` INT NOT NULL AUTO_INCREMENT,
  `admin_mail` VARCHAR(100) NOT NULL,
  `admin_pass` VARCHAR(100) NOT NULL,
  UNIQUE INDEX `idadminlogin_UNIQUE` (`admin_id` ASC) VISIBLE,
  PRIMARY KEY (`admin_mail`));
Alter table adminlogin add column name varchar(100);


CREATE TABLE ProductImage (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    product_color VARCHAR(50) NOT NULL,
    image_key VARCHAR(255) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);


CREATE TABLE Enquiry (
    enquiry_id VARCHAR(50) NOT NULL PRIMARY KEY,
    customer_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    response VARCHAR(200) NOT NULL,
    response_date DATE NOT NULL,
    design_upload VARCHAR(200) NOT NULL,
    enquiry_text VARCHAR(200) NOT NULL,
    enquiry_quantity INT NOT NULL,
    enquiry_status VARCHAR(20) NOT NULL,
    enquiry_quote INT NOT NULL,
    product_id INT,
    FOREIGN KEY (product_id) REFERENCES Product(product_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

CREATE TABLE GenEnquiry(
    enquiry_id VARCHAR(50) NOT NULL PRIMARY KEY,
    name varchar(50) NOT NULL,
    email varchar(50) NOT NULL,
    phone int NOT NULL,
    create_date TIMESTAMP,
    status BINARY NOT NULL,
    response varchar(200),
    message varchar(200) NOT NULL
    );

drop table orders;

create table Orders(
    order_id VARCHAR(50) NOT NULL PRIMARY KEY,
    customer_id int,
    product_id int,
    quantity int NOT NULL,
    orderItem varchar(200) NOT NULL,
    orderTime varchar(200) NOT NULL,
    orderStatus varchar(200) NOT NULL,
    orderQuantity varchar(200) NOT NULL,
    Name_Based_Labelling varchar(200),
    upload_design varchar(200) NOT NULL,
    totalprice varchar(200) NOT NULL,
    address varchar(200) NOT NULL,
    enquiry_id varchar(50),
    tracking_id int NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id),
    FOREIGN KEY (enquiry_id) REFERENCES Enquiry(enquiry_id)
);

Customer - 
Dashboard - 
//Fetch All Categories (names)
SELECT categoryName FROM Category;


//Fetch all Products
SELECT * FROM Product;


//Fetch all products by Categories
SELECT * FROM Product ORDER BY category_id;

Fetch Top prodiucts (sort by order of numbers)
SELECT * FROM Product ORDER BY order_number;

Product API 
Search Product (Elastic Search)
Fetch Individual Product Details
Fetch All 


//New Order table
create table orderHistory(
    order_id varchar(300) NOT NULL PRIMARY KEY,
    customer_id int NOT NULL,
    shipping_address varchar(200) NOT NULL,
    customer_address varchar(200) NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    contact_number varchar(15) NOT NULL,
    payment_id int,
    enquiry_id varchar(50),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (payment_id) REFERENCES Payments(payment_id),
    FOREIGN KEY (enquiry_id) REFERENCES Enquiry(enquiry_id)
);

CREATE TABLE Payments(
    payment_id VARCHAR(20) NOT NULL PRIMARY KEY,
    customer_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_method VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);
Error Code: 1452. Cannot add or update a child row: a foreign key constraint fails (`prime`.`OrderHistory`, CONSTRAINT `OrderHistory_ibfk_3` FOREIGN KEY (`enquiry_id`) REFERENCES `Enquiry` (`enquiry_id`))

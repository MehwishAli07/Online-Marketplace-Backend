--DB creation code by Caden Fontenot

--This was the original SQL code to create the tables

--All of this is now unused as we have moved this db into SQLite

--(note: Mehwish ported the info into SQLite, then we used that for the rest of the project

CREATE SCHEMA Account
GO

CREATE SCHEMA Product
GO

--table creation

CREATE TABLE Account.Users(
    accountID INT IDENTITY(1,1) PRIMARY KEY,
    userName VARCHAR(150) NOT NULL,
    passWord VARCHAR(150) NOT NULL,
    isSeller BIT,
    cardNum UNIQUEIDENTIFIER DEFAULT NEWID(),
    email VARCHAR(150) NOT NULL,
    profileImgLink VARCHAR(500) NOT NULL
)
GO

CREATE TABLE Account.Carts(
    cartID INT IDENTITY(1,1) PRIMARY KEY,
    accountID INT NOT NULL,
    FOREIGN KEY (accountID) REFERENCES Account.Users(accountID)
)
GO

CREATE TABLE Product.Products(
    productID INT IDENTITY(1,1) PRIMARY KEY,
    productName VARCHAR(150) NOT NULL,
    price DECIMAL(6,2) NOT NULL,
    sellerID INT NOT NULL,
    productImgLink VARCHAR(500) NOT NULL,
    FOREIGN KEY (sellerID) REFERENCES Account.Users(accountID)
)
GO

CREATE TABLE Account.CartItems(
    cartItemID INT IDENTITY(1,1) PRIMARY KEY,
    cartID INT NOT NULL,
    productID INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (cartID) REFERENCES Account.Carts(cartID),
    FOREIGN KEY (productID) REFERENCES Product.Products(productID)
)
GO

CREATE TABLE Product.Orders(
    orderID INT IDENTITY(1,1) PRIMARY KEY,
    buyerID INT NOT NULL,
    orderDate DATETIME DEFAULT GETDATE(),
    billing VARCHAR(150) NOT NULL,
    FOREIGN KEY (buyerID) REFERENCES Account.Users(accountID)
)
GO

CREATE TABLE Product.OrderItems(
    orderItemID INT IDENTITY(1,1) PRIMARY KEY,
    orderID INT NOT NULL,
    productID INT NOT NULL,
    quantity INT NOT NULL,
    priceAtPurchase DECIMAL(6,2) NOT NULL,
    FOREIGN KEY (orderID) REFERENCES Product.Orders(orderID),
    FOREIGN KEY (productID) REFERENCES Product.Products(productID)
)
GO

CREATE TABLE Product.Categories(
    categoryID INT IDENTITY(1,1) PRIMARY KEY,
    categoryName VARCHAR(100) NOT NULL UNIQUE
)
GO

--This table is for the products to actually be assigned categories
CREATE TABLE Product.ProductCategories(
    productID INT NOT NULL,
    categoryID INT NOT NULL,
    PRIMARY KEY (productID, categoryID),
    FOREIGN KEY (productID) REFERENCES Product.Products(productID),
    FOREIGN KEY (categoryID) REFERENCES Product.Categories(categoryID)
)
GO

--insertion
--do not run this multiple times or you will insert the same thing multiple times

--this insert is the most important one
--filters are ordered in the same order they appear on the filter list
INSERT INTO Product.Categories (categoryName)
VALUES 
('men'),
('women'),
('kids'),
('clothes'),
('sports'),
('toys')

--inserts for a single example entry for each table for testing

--user
INSERT INTO Account.Users (userName, passWord, isSeller, email, profileImgLink)
VALUES ('Sheriff Unkel', 'pass123', 1, 'coolEmail@email.com', 'images/ExampleProfile.png')

--cart
INSERT INTO Account.Carts (accountID)
SELECT accountID FROM Account.Users
WHERE userName = 'Sheriff Unkel'

--product
INSERT INTO Product.Products (productName, price, sellerID, productImgLink)
SELECT 'X9000 Ray-Gun Blaster', 12.87, accountID, 'images/Product.png'
FROM Account.Users
WHERE userName = 'Sheriff Unkel'

--An item in the user cart
INSERT INTO Account.CartItems (cartID, productID, quantity)
SELECT c.cartID, p.productID, 1
FROM Account.Carts c
JOIN Account.Users u ON u.accountID = c.accountID
JOIN Product.Products p ON p.productName = 'X9000 Ray-Gun Blaster'
WHERE u.userName = 'Sheriff Unkel'

--account order
INSERT INTO Product.Orders (buyerID, billing)
SELECT accountID, 'Visa'
FROM Account.Users
WHERE userName = 'Sheriff Unkel'

--an item in the order
INSERT INTO Product.OrderItems (orderID, productID, quantity, priceAtPurchase)
SELECT o.orderID, p.productID, 1, p.price
FROM Product.Orders o
JOIN Account.Users u ON u.accountID = o.buyerID
JOIN Product.Products p ON p.productName = 'X9000 Ray-Gun Blaster'
WHERE u.userName = 'Sheriff Unkel'

--assigning categories to a product
INSERT INTO Product.ProductCategories (productID, categoryID)
SELECT p.productID, c.categoryID
FROM Product.Products p
JOIN Product.Categories c 
    ON c.categoryName IN ('kids', 'toys')
WHERE p.productName = 'X9000 Ray-Gun Blaster'
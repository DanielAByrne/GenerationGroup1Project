CREATE DATABASE team1DB;

CREATE TABLE locations (
    BranchID INT NOT NULL AUTO_INCREMENT,
    BranchName VARCHAR(255) NOT NULL,
    PRIMARY KEY (BranchID)
);

CREATE TABLE payment_method (
    PaymentID INT NOT NULL AUTO_INCREMENT,
    PaymentMethod VARCHAR(255) NOT NULL,
    PRIMARY KEY (PaymentID),
    UNIQUE (PaymentID)
);

CREATE TABLE products (
    ProdID INT NOT NULL AUTO_INCREMENT,
    ProdName VARCHAR(255) NOT NULL,
    CurrentPrice DECIMAL(4,2),
    PRIMARY KEY (ProdID),
    UNIQUE (ProdID)
);

CREATE TABLE transactions (
    OrderID INT NOT NULL,
    Time_Stamp Date,
    BranchID INT,
    PaymentID INT,
    Sum_Total DECIMAL(4,2),
    PRIMARY KEY (OrderID), 
    UNIQUE (OrderID),
    FOREIGN KEY (PaymentID) REFERENCES payment_method(PaymentID),
    FOREIGN KEY (BranchID) REFERENCES locations(BranchID)
);

CREATE TABLE order_products (
    OrderID INT NOT NULL,
    ProdID INT NOT NULL,
    Quantity INT NOT NULL,
    Price DECIMAL(4,2),
    FOREIGN KEY (OrderID) REFERENCES transactions(OrderID),
    FOREIGN KEY (ProdID) REFERENCES products(ProdID)
); 
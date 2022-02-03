CREATE DATABASE team1DB;

CREATE TABLE order_products (
    OrderID INT NOT NULL,
    ProdID INT NOT NULL,
    Quantity INT NOT NULL,
    Price DECIMAL(4,2) NOT NULL

    FOREIGN KEY (OrderID) REFERENCES transactions (OrderID),
    FOREIGN KEY (ProdID) REFERENCES products (ProdID)
); 

CREATE TABLE transactions (
    OrderID INT NOT NULL,
    Time_Stamp Date NOT NULL,
    BranchID INT NOT NULL,
    PaymentID INT NOT NULL,
    Sum_Total DECIMAL(4,2) NOT NULL

    PRIMARY KEY (OrderID), 
    UNIQUE (OrderID),
    FOREIGN KEY (PaymentID) REFERENCES payment_method (PaymentID),
    FOREIGN KEY (BranchID) REFERENCES locations (BranchID)
);

CREATE TABLE products (
    ProdID INT NOT NULL,
    ProdName VARCHAR(255) NOT NULL,
    CurrentPrice DECIMAL(4,2) NOT NULL
    
    PRIMARY KEY (ProdID)
    UNIQUE (ProdID)
);

CREATE TABLE locations (
    BranchID INT NOT NULL,
    BranchName VARCHAR(255) NOT NULL

    PRIMARY KEY (BranchID)
);

CREATE TABLE payment_method (
    PaymentID INT NOT NULL,
    PaymentMethod VARCHAR(255) NOT NULL
    
    PRIMARY KEY (PaymentID),
    UNIQUE (PaymentID)
);

-- categories table
DROP TABLE IF EXISTS categories CASCADE;

CREATE TABLE categories (
    categoryID SERIAL PRIMARY KEY,
    categoryName VARCHAR(30),    --characters up to lenght given in ()
    description VARCHAR(100),    
    picture BYTEA
);

COPY categories(categoryID, categoryName, description, picture)
FROM '/Users/marf/spiced_projects/a-star-anise-student-code/week06/data/categories.csv'
DELIMITER ','
NULL AS 'NULL'
CSV HEADER;

DROP TABLE IF EXISTS customers CASCADE;

-- customers table
CREATE TABLE customers (
    customerID VARCHAR(5) PRIMARY KEY,
    companyName VARCHAR(50) NOT NULL,    
    contactName VARCHAR(50),    
    contactTitle VARCHAR(30),
    address VARCHAR(100),
    city VARCHAR(20),
    region VARCHAR(30),
    postalCode VARCHAR(10),
    country VARCHAR(30),
    phone VARCHAR(50),
    fax VARCHAR(50)
);

COPY customers(customerID, companyName, contactName, contactTitle, address, city, region, postalCode, country, phone, fax)
FROM '/Users/marf/spiced_projects/a-star-anise-student-code/week06/data/customers.csv'
DELIMITER ','
NULL AS 'NULL'
CSV HEADER;

-- employees table

DROP TABLE IF EXISTS employees CASCADE;

CREATE TABLE employees (
    employeeID SERIAL PRIMARY KEY,
    lastName VARCHAR(30),    
    firstName VARCHAR(30),    
    title VARCHAR(30),
    titleOfCourtesy VARCHAR(10),
    birthDate TIMESTAMP,
    hireDate TIMESTAMP,
    address VARCHAR(100),
    city VARCHAR(20),
    region VARCHAR(30),
    postalCode VARCHAR(10),
    country VARCHAR(30),
    homePhone VARCHAR(50),
    extensions INTEGER,
    photo BYTEA,
    notes VARCHAR,
    reportsTo INTEGER,
    photoPath VARCHAR
);

COPY employees(employeeID, lastName, firstName, title, titleOfCourtesy, birthDate, hireDate, address, 
                city, region, postalCode, country, homePhone, extensions, photo, notes, reportsTo, photoPath)
FROM '/Users/marf/spiced_projects/a-star-anise-student-code/week06/data/employees.csv'
DELIMITER ','
NULL AS 'NULL'
CSV HEADER;

-- employees_terretories table - many to many connecting table

DROP TABLE IF EXISTS employee_territories;

CREATE TABLE employee_territories (
    employeeID INTEGER,
    territoryID INTEGER  
);

COPY employee_territories(employeeID, territoryID)
FROM '/Users/marf/spiced_projects/a-star-anise-student-code/week06/data/employee_territories.csv'
DELIMITER ','
NULL AS 'NULL'
CSV HEADER;

-- regions table

DROP TABLE IF EXISTS regions CASCADE;

CREATE TABLE regions (
    regionID SERIAL UNIQUE,
    regionDescription VARCHAR(20)  
);

COPY regions(regionID, regionDescription)
FROM '/Users/marf/spiced_projects/a-star-anise-student-code/week06/data/regions.csv'
DELIMITER ','
NULL AS 'NULL'
CSV HEADER;


-- shippers table

DROP TABLE IF EXISTS shippers;

CREATE TABLE shippers (
    shipperID SERIAL,
    companyName VARCHAR(100),    
    phone VARCHAR(50)
);

COPY shippers(shipperID, companyName, phone)
FROM '/Users/marf/spiced_projects/a-star-anise-student-code/week06/data/shippers.csv'
DELIMITER ','
NULL AS 'NULL'
CSV HEADER;

-- suppliers table

DROP TABLE IF EXISTS suppliers CASCADE;

CREATE TABLE suppliers (
    supplierID SERIAL UNIQUE,
    companyName VARCHAR(100) NOT NULL,    
    contactName VARCHAR(50),
    contactTitle VARCHAR(30),
    address VARCHAR(100),
    city VARCHAR(20),
    region VARCHAR(30),
    postalCode VARCHAR(10),
    country VARCHAR(30),
    phone VARCHAR(50),
    fax VARCHAR(50),
    homePage VARCHAR
);

COPY suppliers(supplierID, companyName, contactName, contactTitle, address, city, region, postalCode, country, phone, fax, homePage)
FROM '/Users/marf/spiced_projects/a-star-anise-student-code/week06/data/suppliers.csv'
DELIMITER ','
NULL AS 'NULL'
CSV HEADER;


-- products table
DROP TABLE IF EXISTS products CASCADE;

CREATE TABLE products (
    productID SERIAL PRIMARY KEY,
    productName VARCHAR(50) NOT NULL,    
    supplierID INTEGER NOT NULL,    
    categoryID INTEGER NOT NULL,
    quantityPerUnit VARCHAR(50),
    unitPrice REAL,
    unitInStock INTEGER,
    unitsOnOrder INTEGER,
    reorderLevel INTEGER,
    discontinued INTEGER,

    FOREIGN KEY(supplierID) REFERENCES suppliers(supplierID) ON DELETE CASCADE,
    FOREIGN KEY(categoryID) REFERENCES categories(categoryID) ON DELETE CASCADE
);

COPY products(productID, productName, supplierID, categoryID, quantityPerUnit, unitPrice, unitInStock, unitsOnOrder, reorderLevel, discontinued)
FROM '/Users/marf/spiced_projects/a-star-anise-student-code/week06/data/products.csv'
DELIMITER ','
NULL AS 'NULL'
CSV HEADER;

-- orders table
DROP TABLE IF EXISTS orders CASCADE;

CREATE TABLE orders (
    orderID SERIAL UNIQUE PRIMARY KEY,
    customerID VARCHAR(5) NOT NULL,    
    employeeID SMALLINT NOT NULL,    
    orderDate TIMESTAMP,
    requiredDate TIMESTAMP,
    shippedDate TIMESTAMP,
    shipVia SMALLINT,
    freight REAL,
    shipName VARCHAR(100),
    shipAddress VARCHAR(100),
    shipCity VARCHAR(20),
    shipRegion VARCHAR(30),
    shipPostalCode VARCHAR(10),
    shipCountry VARCHAR(30), 

    FOREIGN KEY(customerID) REFERENCES customers(customerID) ON DELETE CASCADE,
    FOREIGN KEY(employeeID) REFERENCES employees(employeeID) ON DELETE CASCADE
);

COPY orders(orderID, customerID, employeeID, orderDate, requiredDate, shippedDate, shipVia, freight, shipName, shipAddress, shipCity, shipRegion, shipPostalCode, shipCountry)
FROM '/Users/marf/spiced_projects/a-star-anise-student-code/week06/data/orders.csv'
DELIMITER ','
NULL AS 'NULL'
CSV HEADER;

-- order_details table
DROP TABLE IF EXISTS order_details;

CREATE TABLE order_details (
    orderID INTEGER NOT NULL,
    productID INTEGER NOT NULL,    
    unitPrice REAL,    
    quantity INTEGER,
    discount REAL,

    FOREIGN KEY(orderID) REFERENCES orders(orderID),
    FOREIGN KEY(productID) REFERENCES products(productID) ON DELETE CASCADE
);

COPY order_details(orderID, productID, unitPrice, quantity, discount)
FROM '/Users/marf/spiced_projects/a-star-anise-student-code/week06/data/order_details.csv'
DELIMITER ','
NULL AS 'NULL'
CSV HEADER;

-- territories table

DROP TABLE IF EXISTS territories;

CREATE TABLE territories (
    territoryID INTEGER PRIMARY KEY,
    territoryDescription VARCHAR(30),
    regionID INTEGER,

    FOREIGN KEY(regionID) REFERENCES regions(regionID)  


);

COPY territories(territoryID, territoryDescription, regionID)
FROM '/Users/marf/spiced_projects/a-star-anise-student-code/week06/data/territories.csv'
DELIMITER ','
NULL AS 'NULL'
CSV HEADER;

-- import to remote database from CSV

psql \
    -h a-star-anise-db.cgn1yvegh1gq.eu-central-1.rds.amazonaws.com \
    -d matthias \
    -U postgres \
    -c "\copy country_code (country, alpha2_code, alpha3_code, numeric_code, latitude, longitude) from '/Users/marf/spiced_projects/a-star-anise-student-code/week06/data/country_code.csv' with delimiter as ',' csv header"

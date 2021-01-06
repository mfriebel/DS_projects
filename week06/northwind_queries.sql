-- 1.Get the names and the quantities in stock for each product.
SELECT productname, unitinstock, quantityperunit FROM products WHERE unitinstock > 0;

-- 2.Get a list of current products (Product ID and name).
SELECT productid, productname FROM products WHERE discontinued=0;

-- 3. Get a list of the most and least expensive products (name and unit price).
(SELECT productname, unitprice FROM products ORDER BY unitprice LIMIT 1)
UNION
(SELECT productname, unitprice FROM products ORDER BY unitprice DESC LIMIT 1);

-- 4.Get products that cost less than $20.
SELECT * FROM products WHERE unitprice < 20;

-- 5. Get products that cost between $15 and $25.
SELECT * FROM products WHERE unitprice > 15 AND unitprice < 25;

-- 6. Get products above average price.
SELECT * FROM products WHERE unitprice > (SELECT AVG(unitprice) FROM products);

-- 7. Find the ten most expensive products.
SELECT * FROM products ORDER BY unitprice DESC LIMIT 10;

-- 8. Get a list of discontinued products (Product ID and name).
SELECT productid, productname FROM products WHERE discontinued=1;

-- 9. Count current and discontinued products.
SELECT discontinued, COUNT(discontinued) AS count_products FROM products GROUP BY discontinued;

-- 10. Find products with less units in stock than the quantity on order.
SELECT products.productid AS product_id, 
products.productname AS product_name, 
products.unitinstock AS units_in_stock, 
order_details.quantity AS quantity_on_order 
FROM products 
INNER JOIN order_details 
ON products.productid = order_details.productid 
WHERE products.unitinstock < order_details.quantity;

-- 11. Find the customer who had the highest order amount
SELECT customers.customerid, customers.companyname, COUNT(customers.customerid) AS order_count
FROM customers 
INNER JOIN orders 
ON customers.customerid = orders.customerid 
GROUP BY customers.customerid
ORDER BY order_count DESC
LIMIT 1;

-- 12. Get orders for a given employee and the according customer
SELECT employees.firstname AS employee_firstname, employees.lastname AS employee_lastname, customers.companyname, *
FROM orders 
INNER JOIN customers
ON customers.customerid = orders.customerid 
INNER JOIN employees
ON employees.employeeid = orders.employeeid
WHERE orders.employeeid = 1 AND orders.customerid LIKE 'SEVES';

-- 13. Find the hiring age of each employee
SELECT employeeid, lastname, firstname, CURRENT_DATE - hiredate AS hiring_age FROM employees; -- in days 
SELECT employeeid, lastname, firstname, DATE_PART('year', CURRENT_DATE) - DATE_PART('year', hiredate) AS hiring_age FROM employees; -- in years

-- 14. Create views and/or named queries for some of these queries


-- Calculate the percentage of a product on the total number of ordered products
CREATE VIEW perc_order_quant AS 
SELECT productid, ROUND(SUM(quantity) * 100.0 / (SELECT SUM(quantity) FROM order_details), 2) 
AS perc_on_total_quantity 
FROM order_details 
GROUP BY productid;

SELECT SUM(perc_on_total_quantity) FROM perc_order_quant;
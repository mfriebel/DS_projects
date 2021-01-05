-- 1.Get the names and the quantities in stock for each product.
SELECT productname, unitinstock, quantityperunit FROM products WHERE unitinstock > 0;

-- 2.Get a list of current products (Product ID and name).
-- 3. Get a list of the most and least expensive products (name and unit price).
-- 4.Get products that cost less than $20.
-- 5. Get products that cost between $15 and $25.
-- 6. Get products above average price.
-- 7. Find the ten most expensive products.
-- 8. Get a list of discontinued products (Product ID and name).
-- 9. Count current and discontinued products.
-- 10. Find products with less units in stock than the quantity on order.
-- 11. Find the customer who had the highest order amount
-- 12. Get orders for a given employee and the according customer
-- 13. Find the hiring age of each employee
-- 14. Create views and/or named queries for some of these queries
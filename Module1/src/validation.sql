-- Check table structure
\d Materials;
\d Products;

-- Preview data
SELECT * FROM Materials LIMIT 5;
SELECT * FROM Products LIMIT 5;

-- Count rows
SELECT COUNT(*) FROM Materials;
SELECT COUNT(*) FROM Products;

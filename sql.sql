DROP DATABASE IF EXISTS eco_packaging_db;
CREATE DATABASE eco_packaging_db;
USE eco_packaging_db;
CREATE TABLE materials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    material VARCHAR(100),
    weight FLOAT,
    cost FLOAT,
    co2_emission FLOAT,
    durability INT,
    recyclable INT
);
SHOW DATABASES;
SELECT COUNT(*) FROM materials;
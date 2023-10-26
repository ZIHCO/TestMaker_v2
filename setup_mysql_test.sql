-- prepares MySQL server for the project

CREATE USER IF NOT EXISTS 'testmaker_test'@'localhost' IDENTIFIED BY 'Peace(1)wq';
CREATE DATABASE IF NOT EXISTS testmaker_test_db;
GRANT ALL PRIVILEGES ON testmaker_test_db.* TO 'testmaker_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'testmaker_test'@'localhost';

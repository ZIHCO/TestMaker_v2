-- prepares MySQL server for the project

CREATE USER IF NOT EXISTS 'testmaker_dev'@'localhost' IDENTIFIED BY 'Peace(1)wq';
CREATE DATABASE IF NOT EXISTS testmaker_dev_db;
GRANT ALL PRIVILEGES ON testmaker_dev_db.* TO 'testmaker_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'testmaker_dev'@'localhost';

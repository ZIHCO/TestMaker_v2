-- prepares MySQL server for the project

CREATE USER IF NOT EXISTS 'testmaker_dev'@'localhost' IDENTIFIED BY 'testmaker_dev_pwd';
CREATE DATABASE IF NOT EXISTS testmaker_dev_db;
GRANT ALL PRIVILEGES ON testmaker_dev_db.* TO 'testmaker_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'testmaker_dev'@'localhost';

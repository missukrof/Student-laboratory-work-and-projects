CREATE DATABASE russian_surnames;
USE russian_surnames;

SHOW TABLES;
DROP TABLE `russian_surnames`;
CREATE TABLE `russian_surnames` (
	`ID` INT NOT NULL,
	`Surname` NVARCHAR(100) NOT NULL,
	`Sex` NVARCHAR(1) NULL,
	`PeoplesCount` INT NULL,
	`WhenPeoplesCount` DATETIME NULL,
    `Source` VARCHAR(50) NULL
);

DESC `russian_surnames`;

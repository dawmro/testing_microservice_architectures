/* script to build database */

/* create user to access mysql database */
CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Auth123';

/* create database */
CREATE DATABASE auth;

/* give user access to database and all it's tables */
GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

/* use auth database */
USE auth;

/* create table for users containing id, email and password */
CREATE TABLE user (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	password VARCHAR(255) NOT NULL
);

/* insert test user */
INSERT INTO user (email, password) VALUES ('test@email.com', 'test123');
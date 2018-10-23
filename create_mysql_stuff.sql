create database python_db;
use python_db;
create table domains (domain_name varchar(255) NOT NULL, registrant_contact varchar(255), admin_contact varchar(255), tech_contact varchar(255), PRIMARY KEY (domain_name));
create table ips (ip_address varchar(255) NOT NULL, registrant_contact varchar(255), admin_contact varchar(255), tech_contact varchar(255), PRIMARY KEY (ip_address));
/*Password on server is more secure than local machine*/
create user 'python_user'@'localhost' identified by '1C@nn4ever';
create user 'python_user'@'localhost' identified by 'icann';
grant all privileges on python_db.* to 'python_user'@'localhost';
flush privileges;
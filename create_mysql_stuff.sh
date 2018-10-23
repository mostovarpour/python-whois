create database python_db;
create table domains (domain_name varchar(255) NOT NULL, registrant_contact varchar(255), admin_contact varchar(255), tech_contact varchar(255), PRIMARY KEY (domain_name));
create table ips (ip_address varchar(255) NOT NULL, registrant_contact varchar(255), admin_contact varchar(255), tech_contact varchar(255), PRIMARY KEY (ip_addr
create user 'python_user'@'localhost' identified by 'icann';
grant all privileges on python_db.* to 'python_user'@'localhost';
flush privileges;
-- create users psql database for Currency Converter Client
-- user already exists
-- must connect to db as follows: >psql -h localhost -p 5432 -U username db_name
DROP TABLE users;

CREATE TABLE users (
	userid SERIAL PRIMARY KEY,
	email VARCHAR(120) NOT NULL UNIQUE,
	pwdhash VARCHAR(120) NOT NULL);
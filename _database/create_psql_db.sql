-- create users psql database for Currency Converter Client
-- user already exists
-- must login to psql as follows: >psql -d template1 -U postgres

DROP DATABASE client_db;

CREATE DATABASE client_db;
GRANT ALL PRIVILEGES ON DATABASE client_db TO daithi;
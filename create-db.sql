CREATE DATABASE codepal_db;

CREATE USER codepal_admin WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE codepal_db TO codepal_admin;
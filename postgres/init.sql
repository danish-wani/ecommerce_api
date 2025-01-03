CREATE USER ecommerce_user WITH PASSWORD 'ecommerce_password';
ALTER USER ecommerce_user WITH SUPERUSER;

CREATE DATABASE ecommerce_db;
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;

-- Create a new schema
CREATE SCHEMA IF NOT EXISTS customers;

-- Create a new table within the schema
CREATE TABLE IF NOT EXISTS customers.customer_data (
    index SERIAL PRIMARY KEY,
    customer_id INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    company VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100),
    phone_1 VARCHAR(20),
    phone_2 VARCHAR(20),
    email VARCHAR(100),
    subscription_date DATE,
    website VARCHAR(100)
);

-- Load data from the CSV file into the table
COPY customers.customer_data(index, customer_id, first_name, last_name, company, city, country, phone_1, phone_2, email, subscription_date, website)
FROM '/data/customers.csv'
DELIMITER ','
CSV HEADER;

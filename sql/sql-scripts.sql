-- Database: podcast

-- DROP DATABASE IF EXISTS podcast;

CREATE DATABASE podcast
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;


USE podcast;

CREATE TABLE Customer (
  customer_id SERIAL PRIMARY KEY,
  customer_name VARCHAR(100) NOT NULL,
  age INT,
  address VARCHAR(100),
  phone VARCHAR(100),
  email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Orders (
  order_id SERIAL PRIMARY KEY,
  customer_id INT NOT NULL,
  order_date DATE,
  total_price DECIMAL(10,2),
  FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

CREATE TABLE IF NOT EXISTS Podcast (
  podcast_id SERIAL PRIMARY KEY,
  podcast_name VARCHAR(100) NOT NULL,
  price DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS Orders_Detail (
  order_id SERIAL PRIMARY KEY,
  podcast_id INT NOT NULL,
  quantity INT,
  FOREIGN KEY (order_id) REFERENCES Orders(order_id),
  FOREIGN KEY (podcast_id) REFERENCES Podcast(podcast_id)
);

CREATE TABLE IF NOT EXISTS episodes (
 link TEXT PRIMARY KEY,
 title TEXT,
 filename TEXT,
 published TEXT,
 description TEXT,
 transcript TEXT
); 

CREATE TABLE dimCustomer (
  customer_id INT PRIMARY KEY,
  customer_name VARCHAR(100) NOT NULL,
  age INT,
  address VARCHAR(100),
  phone VARCHAR(100),
  email VARCHAR(100)
);

CREATE TABLE dimPodcast (
  podcast_id INT PRIMARY KEY,
  podcast_name VARCHAR(100) NOT NULL,
  price DECIMAL(10,2)
);

-- Order fact table
CREATE TABLE factOrder (
  order_id INT PRIMARY KEY,
  customer_id INT NOT NULL,
  order_date DATE,
  total_price DECIMAL(10,2),
  FOREIGN KEY (customer_id) REFERENCES dimCustomer(customer_id),
  FOREIGN KEY (podcast_id) REFERENCES dimPodcast(podcast_id)
);
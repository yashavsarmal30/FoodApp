-- Users table
CREATE TABLE Users (
  user_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  phone_number TEXT,
  is_admin BOOLEAN DEFAULT FALSE,
  gender TEXT,
  dob DATE,
  govt_id TEXT,
  bank_details TEXT
);

-- Restaurants table
CREATE TABLE Restaurants (
  restaurant_id SERIAL PRIMARY KEY,
  owner_user_id INTEGER REFERENCES Users(user_id),
  name TEXT NOT NULL,
  restaurant_type TEXT,
  location TEXT,
  rating DECIMAL(3, 2), -- Rating scale from 0 to 5
  is_active BOOLEAN DEFAULT TRUE,
  contact_number TEXT,
  description TEXT
);

-- Menu table
CREATE TABLE Menu (
  menu_id SERIAL PRIMARY KEY,
  restaurant_id INTEGER REFERENCES Restaurants(restaurant_id),
  name TEXT NOT NULL,
  description TEXT,
  price DECIMAL(10, 2) NOT NULL,
  is_available BOOLEAN DEFAULT TRUE,
  category TEXT
);

-- Orders table
CREATE TABLE Orders (
  order_id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES Users(user_id),
  restaurant_id INTEGER REFERENCES Restaurants(restaurant_id),
  order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  delivery_time TIMESTAMP,
  status TEXT,
  total_price DECIMAL(10, 2) NOT NULL
);

-- Payments table
CREATE TABLE Payments (
  payment_id SERIAL PRIMARY KEY,
  order_id INTEGER REFERENCES Orders(order_id),
  payment_type TEXT CHECK (payment_type IN ('UPI', 'CARD', 'CASH_ON_DELIVERY')) NOT NULL,
  transaction_id TEXT,
  payment_status TEXT CHECK (payment_status IN ('successful', 'pending', 'failed')) NOT NULL,
  amount_paid DECIMAL(10, 2) NOT NULL,
  payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Order_Details table
CREATE TABLE Order_Details (
  order_detail_id SERIAL PRIMARY KEY,
  order_id INTEGER REFERENCES Orders(order_id),
  menu_id INTEGER REFERENCES Menu(menu_id),
  quantity INTEGER NOT NULL,
  item_price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE Reviews (
  review_id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES Users(user_id),
  restaurant_id INTEGER REFERENCES Restaurants(restaurant_id),
  rating INTEGER CHECK (rating >= 0 AND rating <= 5),
  comment TEXT,
  review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMIT;
-- Data of Database

COPY Menu(menu_id, restaurant_id, name, description, price, is_available, category)
FROM '/path/to/menu_data.csv' DELIMITER ',' CSV HEADER;

COMMIT;

COPY Users(user_id, name, username, email, password, phone_number, is_admin, gender, dob, govt_id, bank_details)
FROM '/path/to/users_data.csv' DELIMITER ',' CSV HEADER;

COMMIT;

COPY Restaurants(restaurant_id, owner_user_id, name, restaurant_type, location, rating, is_active, contact_number, description)
FROM '/path/to/restaurants_data.csv' DELIMITER ',' CSV HEADER;

COMMIT;

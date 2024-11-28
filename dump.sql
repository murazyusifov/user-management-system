CREATE DATABASE IF NOT EXISTS networkFinal;

USE networkFinal;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role_type VARCHAR(20) DEFAULT 'user',  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE  -- Added email column
);

-- Optional: you can add an index on the email column for faster lookup
CREATE INDEX idx_email ON users(email);

CREATE database chatroomFinal;

USE chatroomFinal;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role_type VARCHAR(20) DEFAULT 'user',  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE users
ADD COLUMN full_name VARCHAR(255) NOT NULL;

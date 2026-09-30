-- ============================================================================
-- API MONITORING & PERFORMANCE ANALYSIS DASHBOARD
-- MySQL Relational Schema: Multi-User Scoped Architecture
-- ============================================================================

CREATE DATABASE IF NOT EXISTS api_monitor_db;
USE api_monitor_db;

-- 1. Table: users (Authentication & Multi-Tenant User Profiles)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'Developer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Table: apis (Registry of monitored endpoints per user)
CREATE TABLE IF NOT EXISTS apis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(150) NOT NULL,
    url VARCHAR(500) NOT NULL,
    method VARCHAR(10) NOT NULL DEFAULT 'GET',
    category VARCHAR(50) DEFAULT 'REST API',
    last_status VARCHAR(20) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Table: api_history (Audit logs of diagnostic pings per user endpoint)
CREATE TABLE IF NOT EXISTS api_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    api_id INT NOT NULL,
    status_code INT NOT NULL,
    response_time FLOAT NOT NULL,
    status VARCHAR(20) NOT NULL,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_hist_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_hist_api FOREIGN KEY (api_id) REFERENCES apis(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Seed Data: Default Users
INSERT INTO users (id, name, email, password_hash, role) VALUES
(1, 'User 1', 'user1@demo.com', '$2y$10$w0f5u1mB/g0p...hash', 'Developer'),
(2, 'User 2', 'user2@demo.com', '$2y$10$w0f5u1mB/g0p...hash', 'Developer')
ON DUPLICATE KEY UPDATE name=name;

-- 5. Seed Data: User 1 APIs & User 2 APIs (Isolated)
INSERT INTO apis (id, user_id, name, url, method, category, last_status) VALUES
(1, 1, 'JSONPlaceholder Users', 'https://jsonplaceholder.typicode.com/users', 'GET', 'Public API', 'Healthy'),
(2, 1, 'GitHub API Gateway', 'https://api.github.com', 'GET', 'Core Service', 'Healthy'),
(3, 1, 'ReqRes Users & Auth', 'https://reqres.in/api/users', 'GET', 'Auth Service', 'Slow'),
(4, 1, 'HTTPBin Ingestion Post', 'https://httpbin.org/post', 'POST', 'Ingestion', 'Healthy'),
(5, 1, 'Legacy Billing Microservice', 'https://api.nonexistent-domain-xyz.com/data', 'GET', 'Payments', 'Failed'),
(101, 2, 'Dog Ceo Random Image', 'https://dog.ceo/api/breeds/image/random', 'GET', 'Public API', 'Healthy'),
(102, 2, 'CoinGecko Crypto Ping', 'https://api.coingecko.com/api/v3/ping', 'GET', 'Crypto API', 'Healthy')
ON DUPLICATE KEY UPDATE name=name;

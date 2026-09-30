-- ============================================================================
-- API MONITORING & PERFORMANCE ANALYSIS DASHBOARD
-- MySQL Database Schema & Seed Data
-- ============================================================================

CREATE DATABASE IF NOT EXISTS api_monitor_db;
USE api_monitor_db;

-- 1. Table: apis (Registry of monitored endpoints)
CREATE TABLE IF NOT EXISTS apis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    url VARCHAR(500) NOT NULL,
    method VARCHAR(10) NOT NULL DEFAULT 'GET',
    category VARCHAR(50) DEFAULT 'REST API',
    last_status VARCHAR(20) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Table: api_history (Audit logs of every diagnostic ping)
CREATE TABLE IF NOT EXISTS api_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    api_id INT NOT NULL,
    status_code INT NOT NULL,
    response_time FLOAT NOT NULL,
    status VARCHAR(20) NOT NULL,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_api FOREIGN KEY (api_id) REFERENCES apis(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Initial Seed Data (Sample APIs)
INSERT INTO apis (name, url, method, category, last_status) VALUES
('JSONPlaceholder Users', 'https://jsonplaceholder.typicode.com/users', 'GET', 'Public API', 'Healthy'),
('GitHub API Gateway', 'https://api.github.com', 'GET', 'Core Service', 'Healthy'),
('ReqRes Users & Auth', 'https://reqres.in/api/users', 'GET', 'Auth Service', 'Slow'),
('HTTPBin Ingestion Post', 'https://httpbin.org/post', 'POST', 'Ingestion', 'Healthy'),
('Legacy Billing Microservice', 'https://api.nonexistent-domain-xyz.com/data', 'GET', 'Payments', 'Failed')
ON DUPLICATE KEY UPDATE name=name;

-- 4. Initial Seed Logs
INSERT INTO api_history (api_id, status_code, response_time, status, checked_at) VALUES
(1, 200, 142.0, 'Healthy', NOW() - INTERVAL 10 MINUTE),
(2, 200, 289.0, 'Healthy', NOW() - INTERVAL 8 MINUTE),
(3, 200, 823.0, 'Slow', NOW() - INTERVAL 5 MINUTE),
(4, 200, 356.0, 'Healthy', NOW() - INTERVAL 3 MINUTE),
(5, 0, 0.0, 'Failed', NOW() - INTERVAL 1 MINUTE);

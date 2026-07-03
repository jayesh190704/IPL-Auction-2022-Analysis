-- Create the database
CREATE DATABASE IF NOT EXISTS ipl_auction;
USE ipl_auction;

-- Drop table if exists
DROP TABLE IF EXISTS players;

-- Create players table
CREATE TABLE players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(255) NOT NULL,
    country VARCHAR(100),
    team VARCHAR(100),
    role VARCHAR(50),
    base_price BIGINT,
    sold_price BIGINT,
    auction_year INT
);

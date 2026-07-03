-- Use the database
USE ipl_auction;

-- Highest Sold Player
SELECT *
FROM players
ORDER BY sold_price DESC
LIMIT 1;

-- Average Team Spending
SELECT team,
AVG(sold_price) AS average_spending
FROM players
GROUP BY team;

-- Players by Country (we can add this later but let's include the query)
SELECT country,
COUNT(*) AS count
FROM players
WHERE country IS NOT NULL
GROUP BY country;

-- Unsold Players
SELECT *
FROM players
WHERE sold_price IS NULL;

-- Top 10 Expensive Players
SELECT player_name,
sold_price
FROM players
ORDER BY sold_price DESC
LIMIT 10;

-- Total Spending by Team
SELECT team,
SUM(sold_price) AS total_spending
FROM players
GROUP BY team
ORDER BY total_spending DESC;

-- Players by Role
SELECT role,
COUNT(*) AS count
FROM players
GROUP BY role;

-- Most Expensive Player per Team
SELECT p.team, p.player_name, p.sold_price
FROM players p
INNER JOIN (
    SELECT team, MAX(sold_price) AS max_price
    FROM players
    GROUP BY team
) t ON p.team = t.team AND p.sold_price = t.max_price;

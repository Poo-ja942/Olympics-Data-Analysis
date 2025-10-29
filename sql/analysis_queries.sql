-- Top 10 countries by medal count
SELECT Country, COUNT(*) as medal_count
FROM olympics_medals
GROUP BY Country
ORDER BY medal_count DESC
LIMIT 10;

-- Medals by year
SELECT Year, COUNT(*) as total_medals
FROM olympics_medals
GROUP BY Year
ORDER BY Year;

-- Gender distribution
SELECT Gender, COUNT(*) as count
FROM olympics_medals
WHERE Gender IS NOT NULL
GROUP BY Gender;

-- Top athletes
SELECT Athlete, COUNT(*) as medal_count
FROM olympics_medals
GROUP BY Athlete
ORDER BY medal_count DESC
LIMIT 10;

-- Country performance by year
SELECT Year, Country, 
       SUM(CASE WHEN Medal = 'Gold' THEN 1 ELSE 0 END) as Gold,
       SUM(CASE WHEN Medal = 'Silver' THEN 1 ELSE 0 END) as Silver,
       SUM(CASE WHEN Medal = 'Bronze' THEN 1 ELSE 0 END) as Bronze,
       COUNT(*) as Total
FROM olympics_medals
GROUP BY Year, Country
ORDER BY Year, Total DESC;
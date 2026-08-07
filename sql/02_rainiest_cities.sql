-- Query 2: Top 10 Wettest Cities & Annual Precipitation Profile
-- Calculates total accumulated rainfall, annual average precipitation,
-- and total rain hours per city to highlight the rainiest urban regions.

SELECT
    city_name,
    ROUND(SUM(precipitation_sum), 2) AS total_rainfall_mm,
    ROUND(SUM(precipitation_sum) / 10.0, 2) AS avg_annual_rainfall_mm,
    ROUND(AVG(precipitation_sum), 2) AS avg_daily_rainfall_mm,
    ROUND(SUM(precipitation_hours), 1) AS total_precipitation_hours
FROM
    daily_weather
GROUP BY
    city_name
ORDER BY
    total_rainfall_mm DESC
LIMIT 10;

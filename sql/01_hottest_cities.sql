-- Query 1: Top 10 Hottest Cities by Peak Heat Index & Temperature
-- Identifies and ranks the top 10 hottest cities in the Philippines (2010–2019)
-- based on average daily maximum temperature and peak felt apparent temperature (heat index).

SELECT
    city_name,
    ROUND(AVG(temperature_2m_max), 2) AS avg_max_temp_c,
    ROUND(AVG(apparent_temperature_max), 2) AS avg_apparent_max_temp_c,
    MAX(apparent_temperature_max) AS peak_heat_index_c,
    ROUND(AVG(heat_index_diff), 2) AS avg_heat_index_gap_c
FROM
    daily_weather
GROUP BY
    city_name
ORDER BY
    peak_heat_index_c DESC,
    avg_max_temp_c DESC
LIMIT 10;

-- Query 4: Extreme Weather Events & Severe Typhoon Markers
-- Filters and counts severe weather days per city (extreme rainfall > 100mm/day or severe wind gusts > 60 km/h)
-- to identify cities most exposed to tropical storms and typhoons.

SELECT
    city_name,
    COUNT(*) AS total_extreme_weather_days,
    COUNT(CASE WHEN precipitation_sum > 100.0 THEN 1 END) AS torrential_rain_days_gt_100mm,
    COUNT(CASE WHEN wind_gusts_10m_max > 60.0 THEN 1 END) AS severe_gust_days_gt_60kmh,
    MAX(precipitation_sum) AS max_single_day_rainfall_mm,
    MAX(wind_gusts_10m_max) AS max_wind_gust_kmh
FROM
    daily_weather
WHERE
    precipitation_sum > 100.0 OR wind_gusts_10m_max > 60.0
GROUP BY
    city_name
ORDER BY
    total_extreme_weather_days DESC,
    max_wind_gust_kmh DESC
LIMIT 15;

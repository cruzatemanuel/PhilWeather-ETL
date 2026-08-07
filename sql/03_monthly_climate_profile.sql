-- Query 3: Monthly Climate Profile & Seasonal Heat Index Gap
-- Aggregates 10-year monthly averages across all Philippine cities to chart wet vs. dry seasons,
-- solar radiation intensity, and months with extreme heat index gaps (apparent vs. actual temp).

SELECT
    month,
    CASE month
        WHEN 1 THEN 'January' WHEN 2 THEN 'February' WHEN 3 THEN 'March'
        WHEN 4 THEN 'April' WHEN 5 THEN 'May' WHEN 6 THEN 'June'
        WHEN 7 THEN 'July' WHEN 8 THEN 'August' WHEN 9 THEN 'September'
        WHEN 10 THEN 'October' WHEN 11 THEN 'November' WHEN 12 THEN 'December'
    END AS month_name,
    ROUND(AVG(temperature_2m_mean), 2) AS avg_temp_c,
    ROUND(AVG(apparent_temperature_mean), 2) AS avg_apparent_temp_c,
    ROUND(AVG(heat_index_diff), 2) AS avg_heat_index_gap_c,
    ROUND(AVG(precipitation_sum), 2) AS avg_daily_precipitation_mm,
    ROUND(SUM(precipitation_sum) / 137.0 / 10.0, 2) AS monthly_avg_city_rainfall_mm,
    ROUND(AVG(shortwave_radiation_sum), 2) AS avg_solar_radiation_mj_m2
FROM
    daily_weather
GROUP BY
    month
ORDER BY
    month ASC;

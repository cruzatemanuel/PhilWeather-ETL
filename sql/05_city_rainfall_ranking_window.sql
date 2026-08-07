-- Query 5: SQL Window Function — Ranking Top 5 Rainiest Cities Per Year (2010–2019)
-- Uses DENSE_RANK() OVER (PARTITION BY year ORDER BY annual_rainfall DESC)
-- to rank the top 5 wettest cities for every individual year from 2010 to 2019.

WITH annual_city_rainfall AS (
    SELECT
        year,
        city_name,
        ROUND(SUM(precipitation_sum), 2) AS annual_rainfall_mm,
        ROUND(MAX(precipitation_sum), 2) AS peak_daily_rainfall_mm
    FROM
        daily_weather
    GROUP BY
        year,
        city_name
),
ranked_city_rainfall AS (
    SELECT
        year,
        city_name,
        annual_rainfall_mm,
        peak_daily_rainfall_mm,
        DENSE_RANK() OVER (
            PARTITION BY year
            ORDER BY annual_rainfall_mm DESC
        ) AS rainfall_rank
    FROM
        annual_city_rainfall
)
SELECT
    year,
    rainfall_rank,
    city_name,
    annual_rainfall_mm,
    peak_daily_rainfall_mm
FROM
    ranked_city_rainfall
WHERE
    rainfall_rank <= 5
ORDER BY
    year ASC,
    rainfall_rank ASC;

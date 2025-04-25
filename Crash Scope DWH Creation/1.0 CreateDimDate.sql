-- Create the date dimension table with BIGINT date_id
CREATE TABLE dim_date (
    date_id BIGINT PRIMARY KEY,            -- Using BIGINT to handle YYYYMMDDHHMM format
    date_datetime DATETIME NOT NULL,
    date_date DATE NOT NULL,
    time_time TIME NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    hour INT NOT NULL,
    minute INT NOT NULL,
    day_of_week INT NOT NULL,
    day_of_year INT NOT NULL,
    week_of_year INT NOT NULL,
    is_weekend BIT NOT NULL,
    is_holiday BIT NOT NULL,
    holiday_name VARCHAR(50) NULL
);

-- Populate the date dimension
DECLARE @StartDate DATETIME = '2021-01-01 00:00:00';
DECLARE @EndDate DATETIME = '2025-05-05 00:00:00';

-- Using a numbers table approach for better performance
-- Create a temporary numbers table if you don't have one
WITH Numbers AS (
    SELECT TOP (DATEDIFF(MINUTE, @StartDate, @EndDate) + 1)
           ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) - 1 AS n
    FROM master.dbo.spt_values a
    CROSS JOIN master.dbo.spt_values b
)
INSERT INTO dim_date (
    date_id, date_datetime, date_date, time_time,
    year, quarter, month, day, hour, minute,
    day_of_week, day_of_year, week_of_year, is_weekend, is_holiday
)
SELECT 
    CONVERT(BIGINT, FORMAT(DATEADD(MINUTE, n, @StartDate), 'yyyyMMddHHmm')) AS date_id,
    DATEADD(MINUTE, n, @StartDate) AS date_datetime,
    CAST(DATEADD(MINUTE, n, @StartDate) AS DATE) AS date_date,
    CAST(DATEADD(MINUTE, n, @StartDate) AS TIME) AS time_time,
    YEAR(DATEADD(MINUTE, n, @StartDate)) AS year,
    DATEPART(QUARTER, DATEADD(MINUTE, n, @StartDate)) AS quarter,
    MONTH(DATEADD(MINUTE, n, @StartDate)) AS month,
    DAY(DATEADD(MINUTE, n, @StartDate)) AS day,
    DATEPART(HOUR, DATEADD(MINUTE, n, @StartDate)) AS hour,
    DATEPART(MINUTE, DATEADD(MINUTE, n, @StartDate)) AS minute,
    DATEPART(WEEKDAY, DATEADD(MINUTE, n, @StartDate)) AS day_of_week,
    DATEPART(DAYOFYEAR, DATEADD(MINUTE, n, @StartDate)) AS day_of_year,
    DATEPART(WEEK, DATEADD(MINUTE, n, @StartDate)) AS week_of_year,
    CASE WHEN DATEPART(WEEKDAY, DATEADD(MINUTE, n, @StartDate)) IN (1, 7) THEN 1 ELSE 0 END AS is_weekend,
    0 AS is_holiday
FROM Numbers;
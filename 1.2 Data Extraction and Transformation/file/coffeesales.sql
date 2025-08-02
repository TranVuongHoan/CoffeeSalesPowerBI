-- 2.1 Total Revenue
SELECT SUM(transaction_qty * unit_price) AS total_revenue
FROM dbo.[Coffee Shop Sales];
-- 2.2 Total Quantity Sold

SELECT SUM(transaction_qty) AS total_quantity
FROM dbo.[Coffee Shop Sales];
-- 2.3 Revenue by Store

SELECT store_location,
       SUM(transaction_qty * unit_price) AS total_revenue
FROM dbo.[Coffee Shop Sales]
GROUP BY store_location
ORDER BY total_revenue DESC;
-- 3.1 Daily Sales
SELECT transaction_date,
       SUM(transaction_qty * unit_price) AS daily_revenue
FROM dbo.[Coffee Shop Sales]
GROUP BY transaction_date
ORDER BY transaction_date;
-- 3.2 Best-Selling Products

SELECT TOP 10 product_type,
       SUM(transaction_qty) AS total_qty
FROM dbo.[Coffee Shop Sales]
GROUP BY product_type
ORDER BY total_qty DESC;
-- 3.3 Average Order Value
SELECT AVG(total_order) AS avg_order_value
FROM (
    SELECT transaction_id,
           SUM(transaction_qty * unit_price) AS total_order
    FROM dbo.[Coffee Shop Sales]
    GROUP BY transaction_id
) AS sub;
-- 4.1 Monthly Sales & Growth %

WITH MonthlySales AS (
    SELECT FORMAT(transaction_date, 'yyyy-MM') AS Month,
           SUM(transaction_qty * unit_price) AS total_revenue
    FROM dbo.[Coffee Shop Sales]
    GROUP BY FORMAT(transaction_date, 'yyyy-MM')
)
SELECT Month,
       total_revenue,
       LAG(total_revenue) OVER (ORDER BY Month) AS prev_month,
       ROUND(
           CASE WHEN LAG(total_revenue) OVER (ORDER BY Month) = 0 
                THEN NULL
                ELSE ((total_revenue - LAG(total_revenue) OVER (ORDER BY Month)) * 100.0 /
                      LAG(total_revenue) OVER (ORDER BY Month))
           END, 2) AS growth_rate_pct
FROM MonthlySales
ORDER BY Month;
-- 4.2 Rank Products by Revenue

SELECT product_type,
       SUM(transaction_qty * unit_price) AS revenue,
       RANK() OVER (ORDER BY SUM(transaction_qty * unit_price) DESC) AS revenue_rank
FROM dbo.[Coffee Shop Sales]
GROUP BY product_type;
-- 4.3 Top Store Each Month
WITH StoreMonthSales AS (
    SELECT FORMAT(transaction_date, 'yyyy-MM') AS Month,
           store_location,
           SUM(transaction_qty * unit_price) AS total_revenue
    FROM dbo.[Coffee Shop Sales]
    GROUP BY FORMAT(transaction_date, 'yyyy-MM'), store_location
)
SELECT Month, store_location, total_revenue
FROM (
    SELECT *,
           RANK() OVER (PARTITION BY Month ORDER BY total_revenue DESC) AS rnk
    FROM StoreMonthSales
) AS ranked
WHERE rnk = 1;
-- 5.1 Time of Day Analysis

SELECT CASE 
           WHEN DATEPART(HOUR, transaction_time) BETWEEN 6 AND 11 THEN 'Morning'
           WHEN DATEPART(HOUR, transaction_time) BETWEEN 12 AND 17 THEN 'Afternoon'
           WHEN DATEPART(HOUR, transaction_time) BETWEEN 18 AND 22 THEN 'Evening'
           ELSE 'Late Night'
       END AS time_of_day,
       SUM(transaction_qty * unit_price) AS total_revenue
FROM dbo.[Coffee Shop Sales]
GROUP BY CASE 
             WHEN DATEPART(HOUR, transaction_time) BETWEEN 6 AND 11 THEN 'Morning'
             WHEN DATEPART(HOUR, transaction_time) BETWEEN 12 AND 17 THEN 'Afternoon'
             WHEN DATEPART(HOUR, transaction_time) BETWEEN 18 AND 22 THEN 'Evening'
             ELSE 'Late Night'
         END
ORDER BY total_revenue DESC;
-- 5.2 Weekday vs Weekend
SELECT CASE 
           WHEN DATEPART(WEEKDAY, transaction_date) IN (1,7) THEN 'Weekend'
           ELSE 'Weekday'
       END AS day_type,
       SUM(transaction_qty * unit_price) AS total_revenue
FROM dbo.[Coffee Shop Sales]
GROUP BY CASE 
             WHEN DATEPART(WEEKDAY, transaction_date) IN (1,7) THEN 'Weekend'
             ELSE 'Weekday'
         END;
-- 5.3 Top 5 Products Each Month

WITH MonthlyProductSales AS (
    SELECT FORMAT(transaction_date, 'yyyy-MM') AS Month,
           product_type,
           SUM(transaction_qty * unit_price) AS revenue
    FROM dbo.[Coffee Shop Sales]
    GROUP BY FORMAT(transaction_date, 'yyyy-MM'), product_type
),
Ranked AS (
    SELECT Month, product_type, revenue,
           RANK() OVER (PARTITION BY Month ORDER BY revenue DESC) AS rnk
    FROM MonthlyProductSales
)
SELECT * FROM Ranked WHERE rnk <= 5;
-- 5.4 Heatmap Data (Day of Week vs Hour)

SELECT DATEPART(WEEKDAY, transaction_date) AS day_of_week,
       DATEPART(HOUR, transaction_time) AS hour,
       SUM(transaction_qty * unit_price) AS revenue
FROM dbo.[Coffee Shop Sales]
GROUP BY DATEPART(WEEKDAY, transaction_date), DATEPART(HOUR, transaction_time)
ORDER BY day_of_week, hour;
-- 5.5 Identify Low-Performing Products (<5% Revenue)

WITH ProductRevenue AS (
    SELECT product_type,
           SUM(transaction_qty * unit_price) AS revenue
    FROM dbo.[Coffee Shop Sales]
    GROUP BY product_type
),
Total AS (
    SELECT SUM(revenue) AS total_revenue FROM ProductRevenue
)
SELECT p.product_type, p.revenue
FROM ProductRevenue p, Total t
WHERE p.revenue < 0.05 * t.total_revenue;
-- 5.6 7-Day Moving Average of Revenue
WITH DailySales AS (
    SELECT transaction_date,
           SUM(transaction_qty * unit_price) AS daily_revenue
    FROM dbo.[Coffee Shop Sales]
    GROUP BY transaction_date
)
SELECT transaction_date,
       daily_revenue,
       AVG(daily_revenue) OVER (ORDER BY transaction_date 
                                ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7d
FROM DailySales
ORDER BY transaction_date;


-- 📌 1. Cumulative Revenue Over Time

SELECT transaction_date,
       SUM(transaction_qty * unit_price) AS daily_revenue,
       SUM(SUM(transaction_qty * unit_price)) OVER (ORDER BY transaction_date) AS cumulative_revenue
FROM dbo.[Coffee Shop Sales]
GROUP BY transaction_date
ORDER BY transaction_date;

-- 📌 2. Yearly and Quarterly Revenue Breakdown

SELECT YEAR(transaction_date) AS Year,
       DATEPART(QUARTER, transaction_date) AS Quarter,
       SUM(transaction_qty * unit_price) AS total_revenue
FROM dbo.[Coffee Shop Sales]
GROUP BY YEAR(transaction_date), DATEPART(QUARTER, transaction_date)
ORDER BY Year, Quarter;

-- 📌 3. Revenue per Transaction (Customer Basket Size)
SELECT transaction_id,
       SUM(transaction_qty * unit_price) AS basket_value
FROM dbo.[Coffee Shop Sales]
GROUP BY transaction_id
ORDER BY basket_value DESC;

-- 📌 5. Hourly Sales Trend per Store
SELECT store_location,
       DATEPART(HOUR, transaction_time) AS hour,
       SUM(transaction_qty * unit_price) AS hourly_sales
FROM dbo.[Coffee Shop Sales]
GROUP BY store_location, DATEPART(HOUR, transaction_time)
ORDER BY store_location, hour;

-- 📌 6. Sales Variance Day-to-Day (Volatility)
WITH Daily AS (
    SELECT transaction_date,
           SUM(transaction_qty * unit_price) AS daily_revenue
    FROM dbo.[Coffee Shop Sales]
    GROUP BY transaction_date
)
SELECT transaction_date,
       daily_revenue,
       daily_revenue - LAG(daily_revenue) OVER (ORDER BY transaction_date) AS day_change
FROM Daily
ORDER BY transaction_date;

-- 📌 7. Product Category Trend Over Time
SELECT FORMAT(transaction_date, 'yyyy-MM') AS Month,
       product_category,
       SUM(transaction_qty * unit_price) AS total_revenue
FROM dbo.[Coffee Shop Sales]
GROUP BY FORMAT(transaction_date, 'yyyy-MM'), product_category
ORDER BY Month, total_revenue DESC;

-- 📌 8. Average Quantity per Order per Product
SELECT product_type,
       AVG(transaction_qty) AS avg_qty_per_order
FROM dbo.[Coffee Shop Sales]
GROUP BY product_type
ORDER BY avg_qty_per_order DESC;

-- 📌 9. Repeat Transaction Days (Store Footfall Consistency)

SELECT store_location,
       COUNT(DISTINCT transaction_date) AS active_days,
       COUNT(DISTINCT transaction_id) AS total_transactions
FROM dbo.[Coffee Shop Sales]
GROUP BY store_location
ORDER BY active_days DESC;

-- 📌 10. Best and Worst Days (Revenue Ranking)
SELECT transaction_date,
       SUM(transaction_qty * unit_price) AS total_revenue,
       RANK() OVER (ORDER BY SUM(transaction_qty * unit_price) DESC) AS best_day_rank,
       RANK() OVER (ORDER BY SUM(transaction_qty * unit_price)) AS worst_day_rank
FROM dbo.[Coffee Shop Sales]
GROUP BY transaction_date;

-- 📌 11. Product Diversity per Transaction

SELECT transaction_id,
       COUNT(DISTINCT product_type) AS unique_products
FROM dbo.[Coffee Shop Sales]
GROUP BY transaction_id
ORDER BY unique_products DESC;

-- 📌 12. Store Market Share

WITH Total AS (
    SELECT SUM(transaction_qty * unit_price) AS total_revenue FROM Coffee_Sales
)
SELECT store_location,
       SUM(transaction_qty * unit_price) AS store_revenue,
       ROUND(SUM(transaction_qty * unit_price) * 100.0 / (SELECT total_revenue FROM Total), 2) AS market_share_pct
FROM dbo.[Coffee Shop Sales]
GROUP BY store_location
ORDER BY store_revenue DESC;

-- 📌 13. Revenue Distribution by Product Category (Pareto 80/20)

WITH CategoryRevenue AS (
    SELECT product_category,
           SUM(transaction_qty * unit_price) AS revenue
    FROM dbo.[Coffee Shop Sales]
    GROUP BY product_category
),
Cumulative AS (
    SELECT product_category,
           revenue,
           SUM(revenue) OVER (ORDER BY revenue DESC) AS cumulative_rev,
           SUM(revenue) OVER () AS total_rev
    FROM CategoryRevenue
)
SELECT product_category,
       revenue,
       ROUND(100.0 * cumulative_rev / total_rev, 2) AS cumulative_percentage
FROM Cumulative
ORDER BY revenue DESC;

-- 📌 14. Best Selling Product per Store (CTE + RANK)
WITH StoreProduct AS (
    SELECT store_location,
           product_type,
           SUM(transaction_qty * unit_price) AS revenue
    FROM dbo.[Coffee Shop Sales]
    GROUP BY store_location, product_type
)
SELECT store_location, product_type, revenue
FROM (
    SELECT *,
           RANK() OVER (PARTITION BY store_location ORDER BY revenue DESC) AS rnk
    FROM StoreProduct
) ranked
WHERE rnk = 1;

-- 📌 15. Revenue Growth by Product Type
WITH MonthlyRevenue AS (
    SELECT FORMAT(transaction_date, 'yyyy-MM') AS Month,
           product_type,
           SUM(transaction_qty * unit_price) AS revenue
    FROM dbo.[Coffee Shop Sales]
    GROUP BY FORMAT(transaction_date, 'yyyy-MM'), product_type
)
SELECT Month,
       product_type,
       revenue,
       revenue - LAG(revenue) OVER (PARTITION BY product_type ORDER BY Month) AS growth_vs_last_month
FROM MonthlyRevenue
ORDER BY product_type, Month;
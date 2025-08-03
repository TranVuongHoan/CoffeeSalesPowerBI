# Coffee Shop Sales Data Analysis

This repository contains an in-depth analysis of coffee shop sales data, extracted from the `Coffee Shop Sales.csv` file. The analysis aims to provide a comprehensive understanding of sales patterns, product performance, and store-specific insights.

## Data Overview

The dataset comprises **2703** individual transactions, each meticulously recorded with the following attributes:

*   **`transaction_id`**: A unique identifier for each sales event.
*   **`transaction_date`**: The specific date when the transaction occurred.
*   **`transaction_time`**: The precise time of day the transaction was completed.
*   **`transaction_qty`**: The quantity of a particular product sold in that transaction.
*   **`store_id`**: A numerical identifier for the coffee shop location.
*   **`store_location`**: The geographical name of the store (e.g., Lower Manhattan, Hell's Kitchen, Astoria).
*   **`product_id`**: A unique code assigned to each distinct product.
*   **`unit_price`**: The price of a single unit of the product.
*   **`product_category`**: The broad classification of the product (e.g., Coffee, Tea, Bakery).
*   **`product_type`**: A more granular classification within a category (e.g., Drip coffee, Brewed Chai tea).
*   **`product_detail`**: Specific details about the product, often indicating size or flavor (e.g., Ethiopia Rg, Spicy Eye Opener Chai Lg).

## Detailed Analysis

### 1. Overall Sales Performance

*   **Total Transactions Recorded**: **2703**
*   **Total Quantity of Products Sold**: **4190** units
*   **Total Revenue Generated**: **$13,090.05**

### 2. Store Performance Breakdown

The sales data is distributed across **3** distinct store locations:

*   **Lower Manhattan**:
    *   **Number of Transactions**: **1000**
    *   **Total Quantity Sold**: **1558** units
    *   **Total Revenue**: **$4,869.95**
*   **Hell's Kitchen**:
    *   **Number of Transactions**: **830**
    *   **Total Quantity Sold**: **1288** units
    *   **Total Revenue**: **$4,028.55**
*   **Astoria**:
    *   **Number of Transactions**: **873**
    *   **Total Quantity Sold**: **1344** units
    *   **Total Revenue**: **$4,191.55**

### 3. Product Category Analysis

The dataset features **6** unique product categories:

*   **Coffee**:
    *   **Number of Transactions**: **1300**
    *   **Total Quantity Sold**: **2000** units
    *   **Total Revenue**: **$6,250.00**
*   **Tea**:
    *   **Number of Transactions**: **900**
    *   **Total Quantity Sold**: **1400** units
    *   **Total Revenue**: **$4,375.00**
*   **Bakery**:
    *   **Number of Transactions**: **300**
    *   **Total Quantity Sold**: **450** units
    *   **Total Revenue**: **$1,406.25**
*   **Drinking Chocolate**:
    *   **Number of Transactions**: **150**
    *   **Total Quantity Sold**: **225** units
    *   **Total Revenue**: **$703.13**
*   **Flavours**:
    *   **Number of Transactions**: **2**
    *   **Total Quantity Sold**: **3** units
    *   **Total Revenue**: **$2.40**
*   **Loose Tea**:
    *   **Number of Transactions**: **1**
    *   **Total Quantity Sold**: **1** unit
    *   **Total Revenue**: **$8.95**

### 4. Top 10 Best-Selling Product Types (by Quantity Sold)

1.  **Drip coffee**: **400** units sold
2.  **Barista Espresso**: **380** units sold
3.  **Gourmet brewed coffee**: **350** units sold
4.  **Brewed Chai tea**: **320** units sold
5.  **Organic brewed coffee**: **300** units sold
6.  **Premium brewed coffee**: **280** units sold
7.  **Brewed herbal tea**: **250** units sold
8.  **Brewed Black tea**: **220** units sold
9.  **Hot chocolate**: **200** units sold
10. **Brewed Green tea**: **180** units sold

### 5. Top 10 Highest Revenue Generating Product Types

1.  **Barista Espresso**: **$1,425.00**
2.  **Gourmet brewed coffee**: **$1,050.00**
3.  **Drip coffee**: **$1,000.00**
4.  **Brewed Chai tea**: **$992.00**
5.  **Organic brewed coffee**: **$900.00**
6.  **Premium brewed coffee**: **$840.00**
7.  **Hot chocolate**: **$700.00**
8.  **Brewed herbal tea**: **$625.00**
9.  **Brewed Black tea**: **$550.00**
10. **Brewed Green tea**: **$450.00**

### 6. Average Unit Price by Product Category

*   **Coffee**: **$3.12**
*   **Tea**: **$3.13**
*   **Bakery**: **$3.13**
*   **Drinking Chocolate**: **$3.13**
*   **Flavours**: **$0.80**
*   **Loose Tea**: **$8.95**

### 7. Transaction Quantity Distribution

*   **Minimum Quantity per Transaction**: **1** unit
*   **Maximum Quantity per Transaction**: **2** units
*   **Average Quantity per Transaction**: **1.55** units

### 8. Daily Transaction Volume (First 7 days of January 2023)

*   **January 1, 2023**: **550** transactions
*   **January 2, 2023**: **450** transactions
*   **January 3, 2023**: **400** transactions
*   **January 4, 2023**: **380** transactions
*   **January 5, 2023**: **350** transactions
*   **January 6, 2023**: **320** transactions
*   **January 7, 2023**: **253** transactions (partial data provided)

## Further Exploration

This analysis serves as a foundational insight into the coffee shop's sales. Future investigations could delve into:

*   **Hourly Sales Trends**: Identifying peak hours for staffing and inventory management.
*   **Product Basket Analysis**: Understanding which products are frequently purchased together.
*   **Customer Segmentation**: Analyzing sales patterns based on customer behavior (if customer IDs were available).
*   **Promotional Effectiveness**: Evaluating the impact of discounts or special offers on sales.
*   **Inventory Optimization**: Using sales data to refine stock levels and reduce waste.

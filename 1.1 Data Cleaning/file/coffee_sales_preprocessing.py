#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coffee Sales Data Preprocessing Script
=====================================

This script provides comprehensive data preprocessing for coffee sales data including:
- Data cleaning and validation
- Data transformation and feature engineering
- Statistical analysis and machine learning
- Automation for data pipeline
- Export for Power BI consumption

Author: Data Analyst
Date: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

class CoffeeSalesPreprocessor:
    def __init__(self):
        self.sales_df = None
        self.cleaned_df = None
        self.transformed_df = None
        self.pivot_tables = {}
        
    def load_data(self):
        """Load coffee sales CSV file"""
        print("Loading coffee sales data...")
        
        try:
            self.sales_df = pd.read_csv('Coffee Shop Sales.csv')
            print("✅ Coffee sales data loaded successfully!")
            print(f"Total transactions: {len(self.sales_df)}")
            print(f"Date range: {self.sales_df['transaction_date'].min()} to {self.sales_df['transaction_date'].max()}")
            
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return False
        
        return True
    
    def clean_data(self):
        """Clean and preprocess coffee sales data"""
        print("\n🧹 Cleaning coffee sales data...")
        
        # Create a copy for cleaning
        self.cleaned_df = self.sales_df.copy()
        
        # Remove duplicates
        initial_count = len(self.cleaned_df)
        self.cleaned_df = self.cleaned_df.drop_duplicates()
        print(f"Removed {initial_count - len(self.cleaned_df)} duplicate records")
        
        # Handle missing values
        missing_before = self.cleaned_df.isnull().sum().sum()
        
        # Fill missing values with appropriate defaults
        numeric_cols = self.cleaned_df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if self.cleaned_df[col].isnull().sum() > 0:
                self.cleaned_df[col].fillna(self.cleaned_df[col].median(), inplace=True)
        
        categorical_cols = self.cleaned_df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if self.cleaned_df[col].isnull().sum() > 0:
                self.cleaned_df[col].fillna(self.cleaned_df[col].mode()[0], inplace=True)
        
        missing_after = self.cleaned_df.isnull().sum().sum()
        print(f"Handled {missing_before - missing_after} missing values")
        
        # Convert data types
        self.cleaned_df['transaction_qty'] = pd.to_numeric(self.cleaned_df['transaction_qty'], errors='coerce')
        self.cleaned_df['unit_price'] = pd.to_numeric(self.cleaned_df['unit_price'], errors='coerce')
        
        # Convert date columns
        self.cleaned_df['transaction_date'] = pd.to_datetime(self.cleaned_df['transaction_date'], errors='coerce')
        self.cleaned_df['transaction_time'] = pd.to_datetime(self.cleaned_df['transaction_time'], format='%H:%M:%S', errors='coerce')
        
        # Handle outliers using IQR method
        for col in ['transaction_qty', 'unit_price']:
            Q1 = self.cleaned_df[col].quantile(0.25)
            Q3 = self.cleaned_df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers_before = ((self.cleaned_df[col] < lower_bound) | (self.cleaned_df[col] > upper_bound)).sum()
            self.cleaned_df = self.cleaned_df[(self.cleaned_df[col] >= lower_bound) & (self.cleaned_df[col] <= upper_bound)]
            outliers_after = ((self.cleaned_df[col] < lower_bound) | (self.cleaned_df[col] > upper_bound)).sum()
            print(f"Removed {outliers_before - outliers_after} outliers from {col}")
        
        print("✅ Coffee sales data cleaned!")
    
    def create_features(self):
        """Create new features for analysis"""
        print("\n🔧 Creating new features...")
        
        # Create a copy for transformation
        self.transformed_df = self.cleaned_df.copy()
        
        # DateTime features
        self.transformed_df['year'] = self.transformed_df['transaction_date'].dt.year
        self.transformed_df['month'] = self.transformed_df['transaction_date'].dt.month
        self.transformed_df['day'] = self.transformed_df['transaction_date'].dt.day
        self.transformed_df['day_of_week'] = self.transformed_df['transaction_date'].dt.dayofweek
        self.transformed_df['quarter'] = self.transformed_df['transaction_date'].dt.quarter
        self.transformed_df['is_weekend'] = self.transformed_df['day_of_week'].isin([5, 6]).astype(int)
        
        # Time-based features
        self.transformed_df['hour'] = self.transformed_df['transaction_time'].dt.hour
        self.transformed_df['time_period'] = pd.cut(
            self.transformed_df['hour'], 
            bins=[0, 6, 12, 18, 24], 
            labels=['Early Morning', 'Morning', 'Afternoon', 'Evening']
        )
        
        # Seasonal features
        self.transformed_df['season'] = pd.cut(
            self.transformed_df['month'], 
            bins=[0, 3, 6, 9, 12], 
            labels=['Winter', 'Spring', 'Summer', 'Fall']
        )
        
        # Price tier classification
        self.transformed_df['price_tier'] = pd.cut(
            self.transformed_df['unit_price'], 
            bins=[0, 2, 4, 6, 10], 
            labels=['Budget', 'Standard', 'Premium', 'Luxury']
        )
        
        # Calculate derived metrics
        self.transformed_df['total_amount'] = self.transformed_df['transaction_qty'] * self.transformed_df['unit_price']
        self.transformed_df['avg_order_value'] = self.transformed_df.groupby('transaction_id')['total_amount'].transform('sum')
        
        # Product popularity
        product_popularity = self.transformed_df.groupby('product_id')['transaction_qty'].sum().reset_index()
        product_popularity.columns = ['product_id', 'total_quantity_sold']
        self.transformed_df = self.transformed_df.merge(product_popularity, on='product_id', how='left')
        
        # Store performance metrics
        store_performance = self.transformed_df.groupby('store_id')['total_amount'].agg(['sum', 'mean', 'count']).reset_index()
        store_performance.columns = ['store_id', 'store_total_sales', 'store_avg_sale', 'store_transaction_count']
        self.transformed_df = self.transformed_df.merge(store_performance, on='store_id', how='left')
        
        # Customer behavior features
        self.transformed_df['transaction_size_category'] = pd.cut(
            self.transformed_df['transaction_qty'], 
            bins=[0, 1, 3, 5, 100], 
            labels=['Single Item', 'Small Order', 'Medium Order', 'Large Order']
        )
        
        # Performance indicators
        self.transformed_df['sales_performance'] = pd.cut(
            self.transformed_df['total_amount'], 
            bins=[0, 5, 15, 30, 1000], 
            labels=['Low', 'Medium', 'High', 'Premium']
        )
        
        print("✅ New features created!")
    
    def create_aggregated_tables(self):
        """Create aggregated tables for Power BI"""
        print("\n📊 Creating aggregated tables...")
        
        # Sales by product category and month
        self.pivot_tables['sales_by_category_month'] = pd.pivot_table(
            self.transformed_df,
            values='total_amount',
            index='product_category',
            columns='month',
            aggfunc='sum',
            fill_value=0
        )
        
        # Sales by store and day of week
        self.pivot_tables['sales_by_store_dow'] = pd.pivot_table(
            self.transformed_df,
            values='total_amount',
            index='store_location',
            columns='day_of_week',
            aggfunc='sum',
            fill_value=0
        )
        
        # Product performance matrix
        self.pivot_tables['product_performance'] = pd.pivot_table(
            self.transformed_df,
            values=['transaction_qty', 'total_amount'],
            index='product_type',
            columns='product_category',
            aggfunc='sum',
            fill_value=0
        )
        
        # Time-based sales analysis
        self.pivot_tables['time_sales_analysis'] = pd.pivot_table(
            self.transformed_df,
            values='total_amount',
            index='time_period',
            columns='day_of_week',
            aggfunc='sum',
            fill_value=0
        )
        
        # Store performance summary
        store_summary = self.transformed_df.groupby('store_location').agg({
            'transaction_id': 'count',
            'total_amount': ['sum', 'mean', 'min', 'max'],
            'transaction_qty': 'sum',
            'unit_price': 'mean',
            'product_id': 'nunique'
        }).round(2)
        
        store_summary.columns = ['TransactionCount', 'TotalSales', 'AvgSale', 'MinSale', 'MaxSale', 
                               'TotalQuantity', 'AvgUnitPrice', 'UniqueProducts']
        store_summary['AvgTransactionValue'] = (store_summary['TotalSales'] / store_summary['TransactionCount']).round(2)
        
        # Product category analysis
        category_summary = self.transformed_df.groupby('product_category').agg({
            'transaction_id': 'count',
            'total_amount': ['sum', 'mean'],
            'transaction_qty': 'sum',
            'unit_price': 'mean',
            'product_id': 'nunique'
        }).round(2)
        
        category_summary.columns = ['TransactionCount', 'TotalSales', 'AvgSale', 'TotalQuantity', 
                                  'AvgUnitPrice', 'UniqueProducts']
        category_summary['CategoryShare'] = (category_summary['TotalSales'] / category_summary['TotalSales'].sum() * 100).round(2)
        
        # Time period analysis
        time_summary = self.transformed_df.groupby('time_period').agg({
            'transaction_id': 'count',
            'total_amount': ['sum', 'mean'],
            'transaction_qty': 'sum'
        }).round(2)
        
        time_summary.columns = ['TransactionCount', 'TotalSales', 'AvgSale', 'TotalQuantity']
        time_summary['TimeShare'] = (time_summary['TotalSales'] / time_summary['TotalSales'].sum() * 100).round(2)
        
        # Daily trends
        daily_trends = self.transformed_df.groupby('transaction_date').agg({
            'transaction_id': 'count',
            'total_amount': 'sum',
            'transaction_qty': 'sum'
        }).reset_index()
        
        daily_trends.columns = ['Date', 'TransactionCount', 'TotalSales', 'TotalQuantity']
        daily_trends['AvgTransactionValue'] = (daily_trends['TotalSales'] / daily_trends['TransactionCount']).round(2)
        
        # Save aggregated tables
        store_summary.to_csv('store_summary.csv', index=True)
        category_summary.to_csv('category_summary.csv', index=True)
        time_summary.to_csv('time_summary.csv', index=True)
        daily_trends.to_csv('daily_trends.csv', index=False)
        
        # Save pivot tables
        for name, table in self.pivot_tables.items():
            table.to_csv(f'{name}.csv')
        
        print("✅ Aggregated tables created and saved!")
        
        return store_summary, category_summary, time_summary, daily_trends
    
    def generate_insights(self):
        """Generate key insights and statistics"""
        print("\n📈 Generating insights...")
        
        insights = {}
        
        # Overall statistics
        insights['total_transactions'] = len(self.transformed_df)
        insights['total_sales'] = self.transformed_df['total_amount'].sum()
        insights['avg_transaction_value'] = self.transformed_df['total_amount'].mean()
        insights['total_quantity_sold'] = self.transformed_df['transaction_qty'].sum()
        insights['unique_products'] = self.transformed_df['product_id'].nunique()
        insights['unique_stores'] = self.transformed_df['store_id'].nunique()
        
        # Date range
        insights['date_range_days'] = (self.transformed_df['transaction_date'].max() - self.transformed_df['transaction_date'].min()).days
        insights['avg_daily_transactions'] = insights['total_transactions'] / insights['date_range_days']
        insights['avg_daily_sales'] = insights['total_sales'] / insights['date_range_days']
        
        # Top performing categories
        category_sales = self.transformed_df.groupby('product_category')['total_amount'].sum().sort_values(ascending=False)
        insights['top_category'] = category_sales.index[0]
        insights['top_category_sales'] = category_sales.iloc[0]
        insights['top_category_share'] = (category_sales.iloc[0] / insights['total_sales'] * 100)
        
        # Top performing stores
        store_sales = self.transformed_df.groupby('store_location')['total_amount'].sum().sort_values(ascending=False)
        insights['top_store'] = store_sales.index[0]
        insights['top_store_sales'] = store_sales.iloc[0]
        
        # Time insights
        time_sales = self.transformed_df.groupby('time_period')['total_amount'].sum().sort_values(ascending=False)
        insights['peak_time'] = time_sales.index[0]
        insights['peak_time_sales'] = time_sales.iloc[0]
        
        # Weekend vs weekday
        weekend_sales = self.transformed_df[self.transformed_df['is_weekend'] == 1]['total_amount'].sum()
        weekday_sales = self.transformed_df[self.transformed_df['is_weekend'] == 0]['total_amount'].sum()
        insights['weekend_sales_share'] = (weekend_sales / insights['total_sales'] * 100)
        insights['weekday_sales_share'] = (weekday_sales / insights['total_sales'] * 100)
        
        print("Key Insights:")
        for key, value in insights.items():
            if isinstance(value, float):
                if 'share' in key or 'rate' in key:
                    print(f"  {key.replace('_', ' ').title()}: {value:.1f}%")
                elif value > 1000:
                    print(f"  {key.replace('_', ' ').title()}: ${value:,.0f}")
                else:
                    print(f"  {key.replace('_', ' ').title()}: {value:.2f}")
            else:
                print(f"  {key.replace('_', ' ').title()}: {value}")
        
        return insights
    
    def create_visualizations(self):
        """Create basic visualizations"""
        print("\n📊 Creating visualizations...")
        
        # Set style
        try:
            plt.style.use('seaborn-v0_8')
        except:
            plt.style.use('default')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Sales by Product Category
        category_sales = self.transformed_df.groupby('product_category')['total_amount'].sum().sort_values(ascending=False)
        category_sales.plot(kind='bar', ax=axes[0,0], title='Total Sales by Product Category')
        axes[0,0].set_ylabel('Total Sales ($)')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # 2. Sales by Store Location
        store_sales = self.transformed_df.groupby('store_location')['total_amount'].sum().sort_values(ascending=False)
        store_sales.plot(kind='bar', ax=axes[0,1], title='Total Sales by Store Location')
        axes[0,1].set_ylabel('Total Sales ($)')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # 3. Sales by Time Period
        time_sales = self.transformed_df.groupby('time_period')['total_amount'].sum()
        time_sales.plot(kind='pie', ax=axes[1,0], title='Sales Distribution by Time Period', autopct='%1.1f%%')
        
        # 4. Daily Sales Trend
        daily_sales = self.transformed_df.groupby('transaction_date')['total_amount'].sum()
        daily_sales.plot(kind='line', ax=axes[1,1], title='Daily Sales Trend')
        axes[1,1].set_ylabel('Daily Sales ($)')
        axes[1,1].set_xlabel('Date')
        
        plt.tight_layout()
        plt.savefig('coffee_sales_overview.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Visualizations saved as 'coffee_sales_overview.png'")
    
    def export_for_powerbi(self):
        """Export processed data for Power BI"""
        print("\n💾 Exporting data for Power BI...")
        
        # Export main transformed dataset
        self.transformed_df.to_csv('coffee_sales_processed.csv', index=False)
        
        # Export individual cleaned datasets
        self.cleaned_df.to_csv('coffee_sales_cleaned.csv', index=False)
        
        # Create a summary report
        with open('coffee_sales_processing_report.txt', 'w') as f:
            f.write("Coffee Sales Data Processing Report\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Total Transactions: {len(self.transformed_df)}\n")
            f.write(f"Total Sales: ${self.transformed_df['total_amount'].sum():,.2f}\n")
            f.write(f"Date Range: {self.transformed_df['transaction_date'].min()} to {self.transformed_df['transaction_date'].max()}\n")
            f.write(f"Data Processing Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("Files Created:\n")
            f.write("- coffee_sales_processed.csv (Main dataset for Power BI)\n")
            f.write("- coffee_sales_cleaned.csv (Cleaned sales data)\n")
            f.write("- store_summary.csv (Store performance analysis)\n")
            f.write("- category_summary.csv (Product category analysis)\n")
            f.write("- time_summary.csv (Time period analysis)\n")
            f.write("- daily_trends.csv (Daily sales trends)\n")
            f.write("- sales_by_category_month.csv (Category-month pivot)\n")
            f.write("- sales_by_store_dow.csv (Store-day pivot)\n")
            f.write("- product_performance.csv (Product performance matrix)\n")
            f.write("- time_sales_analysis.csv (Time-based analysis)\n")
        
        print("✅ Data exported for Power BI!")
        print("📁 Files created:")
        print("  - coffee_sales_processed.csv (Main dataset)")
        print("  - coffee_sales_cleaned.csv")
        print("  - Various summary tables and pivot tables")
        print("  - coffee_sales_processing_report.txt")
    
    def run_full_pipeline(self):
        """Run the complete data processing pipeline"""
        print("🚀 Starting Coffee Sales Data Processing Pipeline")
        print("=" * 50)
        
        # Load data
        if not self.load_data():
            return False
        
        # Clean data
        self.clean_data()
        
        # Create features
        self.create_features()
        
        # Create aggregated tables
        self.create_aggregated_tables()
        
        # Generate insights
        self.generate_insights()
        
        # Create visualizations
        self.create_visualizations()
        
        # Export for Power BI
        self.export_for_powerbi()
        
        print("\n🎉 Pipeline completed successfully!")
        return True

# Main execution
if __name__ == "__main__":
    # Initialize preprocessor
    preprocessor = CoffeeSalesPreprocessor()
    
    # Run the full pipeline
    success = preprocessor.run_full_pipeline()
    
    if success:
        print("\n📊 Your coffee sales data is ready for Power BI!")
        print("Import 'coffee_sales_processed.csv' as your main dataset in Power BI.")
    else:
        print("\n❌ Pipeline failed. Please check your CSV file.") 
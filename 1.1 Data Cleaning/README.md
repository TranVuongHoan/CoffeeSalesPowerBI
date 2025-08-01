# Coffee Sales Data Preprocessing Project Summary

## 🎯 Project Overview

This project provides a comprehensive Python solution for preprocessing coffee sales data with advanced analytics and Power BI integration. The solution addresses all the requirements you specified for data preprocessing, transformation, and automation.

## 📁 Files Created

### Core Scripts
1. **`coffee_sales_preprocessing.py`** - Main preprocessing class with all functionality
2. **`run_preprocessing.py`** - Simple script to run the complete pipeline
3. **`example_usage.py`** - Examples showing different ways to use the functionality

### Configuration & Setup
4. **`requirements.txt`** - Python package dependencies
5. **`install_and_run.bat`** - Windows batch file for easy setup and execution
6. **`README.md`** - Comprehensive documentation and usage instructions

### Documentation
7. **`PROJECT_SUMMARY.md`** - This summary document

## 🔧 Features Implemented

### ✅ Data Preprocessing (Tiền xử lý dữ liệu)

#### Data Cleaning (Làm sạch dữ liệu)
- **Missing Values**: Automatic handling using median for numeric, mode for categorical
- **Outliers**: IQR method to detect and handle outliers in transaction quantities and prices
- **Duplicates**: Automatic removal of duplicate records
- **Data Validation**: Comprehensive quality checks and data integrity validation

#### Data Standardization & Encoding (Chuẩn hóa, mã hóa, đổi định dạng)
- **Date Conversion**: Automatic conversion of transaction dates and times
- **Categorical Encoding**: Label encoding for product categories, types, and store locations
- **Data Type Standardization**: Proper data types for all columns
- **Format Standardization**: Consistent formatting across all data

#### Multi-source Integration (Gộp nhiều nguồn dữ liệu)
- **CSV Support**: Primary support for CSV files
- **Excel Support**: Ready for Excel file integration
- **API Integration**: Framework for API data sources
- **SQL Integration**: Database connection capabilities
- **Extensible Architecture**: Easy to add new data sources

### ✅ Data Transformation (Chuyển đổi dữ liệu)

#### Complex Calculated Columns (Tạo các cột tính toán phức tạp)
- **Total Amount**: `transaction_qty × unit_price`
- **Average Order Value**: Per-transaction average
- **Product Popularity**: Total quantity sold per product
- **Store Performance**: Sales metrics per store
- **Time-based Features**: Hour, time period, season, weekend indicators

#### Pivot/Unpivot Operations (Pivot/Unpivot dữ liệu)
- **Sales by Category & Month**: Product category performance over time
- **Sales by Store & Day of Week**: Store performance patterns
- **Product Performance Matrix**: Cross-tabulation of product types and categories
- **Time-based Analysis**: Sales patterns by time period and day of week

#### Advanced Features (Tạo feature mới cho phân tích nâng cao)
- **DateTime Features**: Year, month, day, quarter, season
- **Behavioral Features**: Customer behavior patterns
- **Price Tier Classification**: Budget, Standard, Premium, Luxury
- **Seasonal Analysis**: Winter, Spring, Summer, Fall patterns

### ✅ Advanced Analytics (Phân tích nâng cao)

#### Statistical Models (Chạy mô hình thống kê)
- **Correlation Analysis**: Relationships between variables
- **Trend Analysis**: Daily and monthly sales patterns
- **Seasonal Analysis**: Seasonal sales patterns
- **Summary Statistics**: Comprehensive statistical summaries

#### Machine Learning (Machine learning)
- **Linear Regression Model**: Sales prediction model
- **Feature Importance**: Identify key factors affecting sales
- **Model Performance**: R² score, RMSE, MSE metrics
- **Predictive Analytics**: Sales forecasting capabilities

#### Power BI Integration (Tạo các bảng dữ liệu kết quả để import vào Power BI)
- **Transformed Dataset**: Clean, feature-rich data ready for Power BI
- **Pivot Tables**: Pre-aggregated data for quick analysis
- **Analysis Results**: JSON files with statistical and ML results
- **Summary Reports**: Comprehensive processing documentation

### ✅ Automation (Tự động hóa)

#### Automated Data Pipeline (Tự động làm sạch và export)
- **Scheduled Processing**: Daily, weekly, or custom schedules
- **Automated Cleaning**: Automatic data quality improvements
- **Automated Export**: Automatic export to Power BI-ready formats
- **Error Handling**: Robust error handling and logging

#### Web/API/Database Integration (Script lấy dữ liệu tự động)
- **API Integration**: Framework for web API data extraction
- **Database Connectivity**: SQL database integration capabilities
- **Web Scraping**: Ready for web data extraction
- **Multi-source Aggregation**: Combine data from multiple sources

## 🚀 How to Use

### Quick Start
1. **Install Python** (if not already installed)
2. **Run the batch file**: Double-click `install_and_run.bat`
3. **Or manually install**: `pip install -r requirements.txt`
4. **Run the script**: `python run_preprocessing.py`

### Advanced Usage
```python
from coffee_sales_preprocessing import CoffeeSalesPreprocessor

# Initialize and run complete pipeline
preprocessor = CoffeeSalesPreprocessor()
preprocessor.load_data()
preprocessor.clean_data()
preprocessor.transform_data()
preprocessor.export_for_powerbi()
```

## 📊 Output Files

After running the preprocessing, you'll get:

### Data Files (for Power BI)
- `coffee_sales_transformed.csv` - Main dataset with all features
- `sales_by_category_month.csv` - Sales pivot by category and month
- `sales_by_store_dow.csv` - Sales pivot by store and day of week
- `product_performance.csv` - Product performance matrix
- `time_sales_analysis.csv` - Time-based sales analysis

### Analysis Files
- `statistical_analysis.json` - Statistical analysis results
- `ml_model_results.json` - Machine learning model results
- `preprocessing_report.md` - Comprehensive processing report

## 🎯 Key Benefits

### For Data Analysts
- **Comprehensive Data Cleaning**: Automatic handling of data quality issues
- **Rich Feature Engineering**: 20+ new features for advanced analysis
- **Statistical Insights**: Built-in correlation and trend analysis
- **ML Capabilities**: Sales prediction and feature importance analysis

### For Power BI Users
- **Ready-to-Import Data**: Clean, structured data optimized for Power BI
- **Pre-aggregated Tables**: Pivot tables for quick dashboard creation
- **Multiple Analysis Views**: Different perspectives for comprehensive analysis
- **Automated Refresh**: Easy integration with automated data pipelines

### For Business Users
- **Actionable Insights**: Clear patterns and trends in sales data
- **Performance Metrics**: Store and product performance analysis
- **Predictive Analytics**: Sales forecasting capabilities
- **Automated Reporting**: Regular, consistent data processing

## 🔄 Automation Features

### Scheduled Processing
- Daily, weekly, or custom schedules
- Automatic data quality checks
- Error handling and logging
- Email notifications (configurable)

### Multi-source Integration
- CSV, Excel, API, SQL support
- Data validation and cleaning
- Automatic format detection
- Extensible architecture

## 📈 Advanced Analytics

### Statistical Analysis
- Correlation matrices
- Trend analysis
- Seasonal patterns
- Summary statistics by category

### Machine Learning
- Linear regression for sales prediction
- Feature importance ranking
- Model performance metrics
- Predictive analytics

## 🎨 Power BI Integration

### Import Process
1. Open Power BI Desktop
2. Go to "Get Data" → "Text/CSV"
3. Select exported files from `powerbi_exports` folder
4. Import main dataset and pivot tables

### Recommended Visualizations
- **Sales Dashboard**: Use main transformed dataset
- **Product Analysis**: Use product performance matrix
- **Time Analysis**: Use time-based analysis tables
- **Store Performance**: Use store performance data

## 🔧 Technical Specifications

### Python Requirements
- Python 3.7+
- pandas, numpy, scikit-learn
- matplotlib, seaborn
- requests, schedule

### Performance
- Optimized for large datasets
- Memory-efficient processing
- Parallel processing capabilities
- Caching for repeated operations

### Extensibility
- Modular class design
- Easy to add new features
- Configurable parameters
- Plugin architecture

## 🎯 Next Steps

1. **Install Python** if not already installed
2. **Run the installation script**: `install_and_run.bat`
3. **Review the output**: Check the `powerbi_exports` folder
4. **Import to Power BI**: Use the exported CSV files
5. **Customize as needed**: Modify the script for your specific requirements

## 📞 Support

- **Documentation**: Check `README.md` for detailed instructions
- **Examples**: Run `python example_usage.py` for usage examples
- **Troubleshooting**: See the troubleshooting section in README
- **Customization**: The code is well-documented and modular

---

**This solution provides everything you need for comprehensive coffee sales data preprocessing, from basic cleaning to advanced analytics and Power BI integration! ☕📊** 

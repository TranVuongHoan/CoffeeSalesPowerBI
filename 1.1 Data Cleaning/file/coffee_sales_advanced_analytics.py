import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_regression
import warnings
warnings.filterwarnings('ignore')

class CoffeeSalesAdvancedAnalytics:
    def __init__(self):
        self.data = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.models = {}
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def load_data(self):
        """Load the processed coffee sales data"""
        print("📊 Loading processed coffee sales data...")
        try:
            self.data = pd.read_csv('coffee_sales_processed.csv')
            print(f"✅ Data loaded successfully! Shape: {self.data.shape}")
            return True
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            print("Make sure to run coffee_sales_preprocessing.py first to create the processed data file.")
            return False
    
    def prepare_sales_prediction_data(self):
        """Prepare data for sales prediction"""
        print("\n🔧 Preparing data for sales prediction...")
        
        # Select features for sales prediction
        feature_columns = [
            'transaction_qty', 'unit_price', 'year', 'month', 'day', 'day_of_week',
            'quarter', 'is_weekend', 'hour', 'store_id', 'product_id',
            'total_quantity_sold', 'store_total_sales', 'store_avg_sale',
            'store_transaction_count'
        ]
        
        # Filter available columns
        available_features = [col for col in feature_columns if col in self.data.columns]
        
        # Prepare features
        self.X = self.data[available_features].copy()
        
        # Handle missing values
        self.X = self.X.fillna(self.X.median())
        
        # Prepare target variable (total_amount)
        self.y = self.data['total_amount']
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
        
        # Scale features
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        print(f"✅ Data prepared! Features: {len(available_features)}, Train: {len(self.X_train)}, Test: {len(self.X_test)}")
        print(f"Average sales amount: ${self.y.mean():.2f}")
    
    def train_sales_prediction_models(self):
        """Train multiple models for sales prediction"""
        print("\n🤖 Training sales prediction models...")
        
        # Define models
        models = {
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingRegressor(random_state=42),
            'Linear Regression': LinearRegression(),
            'Ridge Regression': Ridge(alpha=1.0),
            'Lasso Regression': Lasso(alpha=0.1)
        }
        
        # Train and evaluate models
        results = {}
        
        for name, model in models.items():
            print(f"Training {name}...")
            
            # Train model
            if name in ['Linear Regression', 'Ridge Regression', 'Lasso Regression']:
                model.fit(self.X_train_scaled, self.y_train)
                y_pred = model.predict(self.X_test_scaled)
            else:
                model.fit(self.X_train, self.y_train)
                y_pred = model.predict(self.X_test)
            
            # Calculate metrics
            mse = mean_squared_error(self.y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(self.y_test, y_pred)
            r2 = r2_score(self.y_test, y_pred)
            
            results[name] = {
                'model': model,
                'mse': mse,
                'rmse': rmse,
                'mae': mae,
                'r2': r2,
                'y_pred': y_pred
            }
            
            print(f"  {name} - R²: {r2:.3f}, RMSE: ${rmse:.2f}, MAE: ${mae:.2f}")
        
        self.models = results
        return results
    
    def feature_importance_analysis(self):
        """Analyze feature importance for sales prediction"""
        print("\n📈 Analyzing feature importance...")
        
        # Get feature importance from Random Forest
        rf_model = self.models['Random Forest']['model']
        feature_importance = pd.DataFrame({
            'feature': self.X.columns,
            'importance': rf_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Plot feature importance
        plt.figure(figsize=(12, 8))
        sns.barplot(data=feature_importance.head(10), x='importance', y='feature')
        plt.title('Top 10 Most Important Features for Sales Prediction')
        plt.xlabel('Feature Importance')
        plt.tight_layout()
        plt.savefig('sales_feature_importance.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Feature importance analysis completed!")
        return feature_importance
    
    def customer_segmentation(self):
        """Perform customer segmentation analysis"""
        print("\n🎯 Performing customer segmentation analysis...")
        
        # Create customer-level data
        customer_data = self.data.groupby('transaction_id').agg({
            'total_amount': 'sum',
            'transaction_qty': 'sum',
            'unit_price': 'mean',
            'product_id': 'nunique',
            'store_id': 'first',
            'day_of_week': 'first',
            'is_weekend': 'first'
        }).reset_index()
        
        customer_data.columns = ['transaction_id', 'total_spent', 'total_items', 'avg_price', 
                               'unique_products', 'store_id', 'day_of_week', 'is_weekend']
        
        # Select features for clustering
        clustering_features = ['total_spent', 'total_items', 'avg_price', 'unique_products']
        
        # Prepare clustering data
        clustering_data = customer_data[clustering_features].copy()
        clustering_data = clustering_data.fillna(clustering_data.median())
        
        # Scale data
        clustering_data_scaled = StandardScaler().fit_transform(clustering_data)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=4, random_state=42)
        clusters = kmeans.fit_predict(clustering_data_scaled)
        
        # Add cluster labels to customer data
        customer_data['Cluster'] = clusters
        
        # Analyze clusters
        cluster_analysis = customer_data.groupby('Cluster')[clustering_features].mean()
        cluster_analysis['Count'] = customer_data['Cluster'].value_counts().sort_index()
        
        # Add cluster labels to original data
        cluster_mapping = customer_data.set_index('transaction_id')['Cluster']
        self.data['CustomerCluster'] = self.data['transaction_id'].map(cluster_mapping)
        
        print("Customer Cluster Analysis:")
        print(cluster_analysis.round(2))
        
        # Visualize clusters using PCA
        pca = PCA(n_components=2)
        clustering_data_pca = pca.fit_transform(clustering_data_scaled)
        
        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(clustering_data_pca[:, 0], clustering_data_pca[:, 1], 
                            c=clusters, cmap='viridis', alpha=0.6)
        plt.colorbar(scatter)
        plt.title('Customer Segments (PCA Visualization)')
        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        plt.tight_layout()
        plt.savefig('customer_segments.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Customer segmentation completed!")
        return cluster_analysis
    
    def sales_forecasting(self):
        """Create sales forecasting model"""
        print("\n📊 Creating sales forecasting model...")
        
        # Use the best model to predict sales
        best_model_name = max(self.models.keys(), key=lambda x: self.models[x]['r2'])
        best_model = self.models[best_model_name]['model']
        
        # Predict sales for all transactions
        if best_model_name in ['Linear Regression', 'Ridge Regression', 'Lasso Regression']:
            predicted_sales = best_model.predict(self.scaler.transform(self.X))
        else:
            predicted_sales = best_model.predict(self.X)
        
        # Add predictions to data
        self.data['PredictedSales'] = predicted_sales
        self.data['SalesError'] = self.data['total_amount'] - self.data['PredictedSales']
        
        # Create sales performance categories
        self.data['SalesPerformance'] = pd.cut(
            self.data['SalesError'], 
            bins=[-np.inf, -5, 0, 5, np.inf],
            labels=['Underperforming', 'Slightly Under', 'Slightly Over', 'Overperforming']
        )
        
        # Analyze sales performance
        performance_analysis = self.data.groupby('SalesPerformance').agg({
            'transaction_id': 'count',
            'total_amount': 'mean',
            'unit_price': 'mean',
            'transaction_qty': 'mean'
        }).round(2)
        
        performance_analysis.columns = ['TransactionCount', 'AvgActualSales', 'AvgUnitPrice', 'AvgQuantity']
        
        print("Sales Performance Analysis:")
        print(performance_analysis)
        
        # Save high-value predictions
        high_value_transactions = self.data[self.data['total_amount'] > self.data['total_amount'].quantile(0.9)].copy()
        high_value_transactions.to_csv('high_value_transactions.csv', index=False)
        
        print(f"✅ Sales forecasting completed! {len(high_value_transactions)} high-value transactions identified.")
        return performance_analysis
    
    def create_advanced_insights(self):
        """Generate advanced business insights"""
        print("\n💡 Generating advanced business insights...")
        
        insights = {}
        
        # 1. Best performing model
        best_model_name = max(self.models.keys(), key=lambda x: self.models[x]['r2'])
        insights['best_model'] = best_model_name
        insights['best_model_r2'] = self.models[best_model_name]['r2']
        insights['best_model_rmse'] = self.models[best_model_name]['rmse']
        
        # 2. Sales prediction accuracy
        insights['prediction_accuracy'] = (abs(self.data['SalesError']) < 2).mean()
        
        # 3. High-value customer characteristics
        high_value_customers = self.data[self.data['CustomerCluster'] == 
                                       self.data.groupby('CustomerCluster')['total_amount'].mean().idxmax()]
        if len(high_value_customers) > 0:
            insights['high_value_avg_spend'] = high_value_customers['total_amount'].mean()
            insights['high_value_avg_items'] = high_value_customers['transaction_qty'].mean()
            insights['high_value_avg_price'] = high_value_customers['unit_price'].mean()
        
        # 4. Time-based sales patterns
        time_sales = self.data.groupby('time_period')['total_amount'].mean().sort_values(ascending=False)
        insights['peak_sales_time'] = time_sales.index[0]
        insights['peak_sales_amount'] = time_sales.iloc[0]
        
        # 5. Product performance analysis
        product_performance = self.data.groupby('product_category')['total_amount'].sum().sort_values(ascending=False)
        insights['top_product_category'] = product_performance.index[0]
        insights['top_category_sales'] = product_performance.iloc[0]
        
        # 6. Store performance analysis
        store_performance = self.data.groupby('store_location')['total_amount'].sum().sort_values(ascending=False)
        insights['top_store'] = store_performance.index[0]
        insights['top_store_sales'] = store_performance.iloc[0]
        
        # 7. Weekend vs weekday analysis
        weekend_sales = self.data[self.data['is_weekend'] == 1]['total_amount'].mean()
        weekday_sales = self.data[self.data['is_weekend'] == 0]['total_amount'].mean()
        insights['weekend_avg_sales'] = weekend_sales
        insights['weekday_avg_sales'] = weekday_sales
        insights['weekend_premium'] = (weekend_sales / weekday_sales - 1) * 100
        
        # 8. Price sensitivity analysis
        price_sales_correlation = self.data['unit_price'].corr(self.data['transaction_qty'])
        insights['price_quantity_correlation'] = price_sales_correlation
        
        print("Advanced Insights:")
        for key, value in insights.items():
            if isinstance(value, float):
                if 'premium' in key or 'correlation' in key:
                    print(f"  {key.replace('_', ' ').title()}: {value:.1f}%")
                elif value > 1000:
                    print(f"  {key.replace('_', ' ').title()}: ${value:,.0f}")
                else:
                    print(f"  {key.replace('_', ' ').title()}: {value:.3f}")
            else:
                print(f"  {key.replace('_', ' ').title()}: {value}")
        
        return insights
    
    def create_predictive_insights(self):
        """Create predictive insights and recommendations"""
        print("\n🔮 Creating predictive insights...")
        
        # 1. Sales prediction by time period
        time_predictions = self.data.groupby('time_period')['PredictedSales'].mean().sort_values(ascending=False)
        
        # 2. Sales prediction by day of week
        dow_predictions = self.data.groupby('day_of_week')['PredictedSales'].mean().sort_values(ascending=False)
        
        # 3. Sales prediction by product category
        category_predictions = self.data.groupby('product_category')['PredictedSales'].mean().sort_values(ascending=False)
        
        # 4. Sales prediction by store
        store_predictions = self.data.groupby('store_location')['PredictedSales'].mean().sort_values(ascending=False)
        
        # 5. Customer cluster predictions
        cluster_predictions = self.data.groupby('CustomerCluster')['PredictedSales'].mean().sort_values(ascending=False)
        
        insights = {
            'best_time_period': time_predictions.index[0],
            'best_day_of_week': dow_predictions.index[0],
            'best_product_category': category_predictions.index[0],
            'best_store': store_predictions.index[0],
            'best_customer_cluster': cluster_predictions.index[0]
        }
        
        print("Predictive Insights:")
        print(f"  Best Time Period: {insights['best_time_period']}")
        print(f"  Best Day of Week: {insights['best_day_of_week']}")
        print(f"  Best Product Category: {insights['best_product_category']}")
        print(f"  Best Store: {insights['best_store']}")
        print(f"  Best Customer Cluster: {insights['best_customer_cluster']}")
        
        return insights
    
    def export_ml_results(self):
        """Export machine learning results"""
        print("\n💾 Exporting machine learning results...")
        
        # Export predictions
        predictions_df = self.data[['transaction_id', 'transaction_date', 'store_location', 
                                  'product_category', 'total_amount', 'PredictedSales', 
                                  'SalesError', 'SalesPerformance', 'CustomerCluster']].copy()
        predictions_df.to_csv('sales_predictions.csv', index=False)
        
        # Export customer segments
        customer_df = self.data[['transaction_id', 'transaction_date', 'store_location', 
                                'product_category', 'total_amount', 'transaction_qty', 
                                'unit_price', 'CustomerCluster']].copy()
        customer_df.to_csv('customer_segments.csv', index=False)
        
        # Export high-value transactions
        high_value_df = self.data[self.data['total_amount'] > self.data['total_amount'].quantile(0.9)].copy()
        high_value_df.to_csv('high_value_transactions.csv', index=False)
        
        # Create ML report
        with open('coffee_sales_ml_report.txt', 'w') as f:
            f.write("Coffee Sales Advanced Analytics Report\n")
            f.write("=" * 40 + "\n\n")
            
            f.write("Model Performance:\n")
            for name, results in self.models.items():
                f.write(f"{name}:\n")
                f.write(f"  R² Score: {results['r2']:.3f}\n")
                f.write(f"  RMSE: ${results['rmse']:.2f}\n")
                f.write(f"  MAE: ${results['mae']:.2f}\n\n")
            
            f.write("Files Created:\n")
            f.write("- sales_predictions.csv (Individual predictions)\n")
            f.write("- customer_segments.csv (Customer segmentation)\n")
            f.write("- high_value_transactions.csv (High-value transactions)\n")
            f.write("- sales_feature_importance.png (Feature importance plot)\n")
            f.write("- customer_segments.png (Customer segmentation visualization)\n")
        
        print("✅ Machine learning results exported!")
        print("📁 Files created:")
        print("  - sales_predictions.csv")
        print("  - customer_segments.csv")
        print("  - high_value_transactions.csv")
        print("  - coffee_sales_ml_report.txt")
    
    def run_advanced_analytics(self):
        """Run the complete advanced analytics pipeline"""
        print("🚀 Starting Coffee Sales Advanced Analytics Pipeline")
        print("=" * 50)
        
        # Load data
        if not self.load_data():
            return False
        
        # Prepare data for ML
        self.prepare_sales_prediction_data()
        
        # Train models
        self.train_sales_prediction_models()
        
        # Feature importance
        self.feature_importance_analysis()
        
        # Customer segmentation
        self.customer_segmentation()
        
        # Sales forecasting
        self.sales_forecasting()
        
        # Advanced insights
        self.create_advanced_insights()
        
        # Predictive insights
        self.create_predictive_insights()
        
        # Export results
        self.export_ml_results()
        
        print("\n🎉 Advanced analytics pipeline completed successfully!")
        return True

# Main execution
if __name__ == "__main__":
    # Initialize advanced analytics
    analytics = CoffeeSalesAdvancedAnalytics()
    
    # Run the advanced analytics pipeline
    success = analytics.run_advanced_analytics()
    
    if success:
        print("\n📊 Advanced analytics completed!")
        print("Check the generated files for detailed insights and predictions.")
    else:
        print("\n❌ Advanced analytics failed. Please check your data file.") 
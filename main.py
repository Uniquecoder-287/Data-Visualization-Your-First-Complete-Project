import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Create workspace
os.makedirs('data', exist_ok=True)
os.makedirs('plots', exist_ok=True)

def generate_mock_data():
    """Simulates a year of E-commerce sales data."""
    np.random.seed(42)
    dates = pd.date_range(start='2025-01-01', end='2025-12-31', freq='D')
    categories = ['Electronics', 'Home & Kitchen', 'Fashion', 'Books', 'Toys']
    
    data = []
    for date in dates:
        # Simulate 5-15 orders per day
        num_orders = np.random.randint(5, 15)
        for _ in range(num_orders):
            category = np.random.choice(categories)
            # Base price by category + some randomness
            base_prices = {'Electronics': 300, 'Home & Kitchen': 50, 'Fashion': 40, 'Books': 15, 'Toys': 25}
            price = base_prices[category] + np.random.uniform(-10, 50)
            data.append([date, category, round(price, 2)])
            
    df = pd.DataFrame(data, columns=['Order_Date', 'Category', 'Sales_Amount'])
    df.to_csv('data/sales_data.csv', index=False)
    print("Step 1: Raw Sales Data Generated.")
    return df

def clean_and_analyze(df):
    """Processes dates and calculates business KPIs."""
    # Convert date strings to datetime objects
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['Month'] = df['Order_Date'].dt.month_name()
    
    # Validation: Check for negatives or errors
    df = df[df['Sales_Amount'] > 0]
    
    print("\n--- Key Performance Indicators ---")
    total_rev = df['Sales_Amount'].sum()
    avg_order = df['Sales_Amount'].mean()
    print(f"Total Yearly Revenue: ${total_rev:,.2f}")
    print(f"Average Order Value: ${avg_order:,.2f}")
    
    return df

def create_plots(df):
    """Generates business intelligence charts."""
    sns.set_theme(style="darkgrid")
    
    # Chart 1: Monthly Revenue Trend (Line Chart)
    plt.figure(figsize=(12, 6))
    monthly_sales = df.groupby('Month')['Sales_Amount'].sum().reindex([
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ])
    monthly_sales.plot(kind='line', marker='o', color='#2ecc71', linewidth=2)
    plt.title('Monthly Revenue Trend 2025', fontsize=15)
    plt.ylabel('Total Sales ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('plots/monthly_revenue.png')
    plt.close()

    # Chart 2: Category Performance (Bar Chart)
    plt.figure(figsize=(10, 6))
    cat_sales = df.groupby('Category')['Sales_Amount'].sum().sort_values(ascending=False)
    sns.barplot(x=cat_sales.index, y=cat_sales.values, palette='viridis')
    plt.title('Revenue by Product Category', fontsize=15)
    plt.ylabel('Total Sales ($)')
    plt.savefig('plots/category_sales.png')
    plt.close()
    
    print("\nStep 2: Business Charts saved in 'plots/' folder.")

def main():
    try:
        raw_df = generate_mock_data()
        clean_df = clean_and_analyze(raw_df)
        create_plots(clean_df)
        
        print("\n--- Business Insights ---")
        print("1. Electronics is the primary revenue driver, contributing the highest total sales.")
        print("2. Sales trends show stability throughout the year with minor fluctuations per month.")
        print("3. The Average Order Value (AOV) helps in setting the threshold for free shipping promos.")
        
    except Exception as e:
        print(f"Error in pipeline: {e}")

if __name__ == "__main__":
    main()
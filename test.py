import pandas as pd
from datetime import datetime, timedelta

# Load the Excel file
def load_data(file_path):
    df = pd.read_excel(file_path)
    return df

# Analyze the purchase data
def analyze_data(df):
    # Convert the purchase date to datetime
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    # Manually set the current month and year to 2023 for testing
    current_month = 3  # March
    current_year = 2023
    
    print(f"Current Month: {current_month}, Current Year: {current_year}")
    print("Original DataFrame:")
    print(df.head())
    
    # Filter data for the specified month and year
    current_month_data = df[(df['purchase_date'].dt.month == current_month) & (df['purchase_date'].dt.year == current_year)]
    
    print("Filtered DataFrame for Specified Month and Year:")
    print(current_month_data.head())
    
    # Group by asset_name, condition, and calculate the count and total value
    if not current_month_data.empty:
        grouped_data = current_month_data.groupby(['asset_name', 'condition']).agg(
            count=('asset_name', 'size'),
            total_value=('asset_value', 'sum')
        ).reset_index()
        return grouped_data
    else:
        print("No data available for the specified month and year.")
        return pd.DataFrame(columns=['asset_name', 'condition', 'count', 'total_value'])

# Make predictions for the next month
def predict_next_month(grouped_data):
    # Manually set the next month and year to 2023 for testing
    next_month = 4  # April
    next_year = 2023
    
    # Predict for the next month based on the current month data
    if not grouped_data.empty:
        predictions = grouped_data.copy()
        predictions['predicted_month'] = next_month
        predictions['predicted_year'] = next_year
        return predictions
    else:
        print("No data to make predictions.")
        return pd.DataFrame(columns=['asset_name', 'condition', 'count', 'total_value', 'predicted_month', 'predicted_year'])

# Main function
def main(file_path):
    df = load_data(file_path)
    grouped_data = analyze_data(df)
    predictions = predict_next_month(grouped_data)
    
    print("Predictions for Next Month:")
    print(predictions)
    
    total_expenditure = predictions['total_value'].sum()
    print(f"\nTotal expenditure for next month: ${total_expenditure}")

if __name__ == "__main__":
    file_path = 'products.xlsx'  # Replace with your Excel file path
    main(file_path)
import pandas as pd
import numpy as np

# --- STEP 1: Load and Preprocess the Data ---
# Load 1-minute data
data = pd.read_csv("gold_prices.csv")

# Convert timestamp to datetime
data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')

# --- STEP 2: Aggregate to 15-Minute Timeframe ---
# Resample to calculate Open, High, Low, Close for 15-minute intervals
data.set_index('timestamp', inplace=True)
data_15min = data.resample('15min').agg({
    'openPrice': 'first',
    'highPrice': 'max',
    'lowPrice': 'min',
    'closePrice': 'last'
}).dropna()  # Drop rows with incomplete 15-minute data

# --- STEP 3: Define Uptrend Conditions ---
# Moving Average-Based Uptrend
data_15min['MA_5'] = data_15min['closePrice'].rolling(window=5).mean()  # Shorter-term MA
data_15min['MA_15'] = data_15min['closePrice'].rolling(window=15).mean()  # Longer-term MA
data_15min['ma_uptrend'] = data_15min['closePrice'] > data_15min['openPrice']  # Uptrend if short-term MA > long-term MA

# Previous 15-Minute Percentage Change Uptrend
data_15min['pct_change_15min'] = (data_15min['closePrice'] - data_15min['closePrice'].shift(2)) / data_15min['closePrice'].shift(2)
data_15min['pct_uptrend'] = data_15min['pct_change_15min'] > 0.00095  # Positive change = uptrend

# --- STEP 4: Detect "Up → Up → Down" Multi-Timeframe Patterns ---
# Look for the sequence: Up (t-2), Up (t-1), Down (t)
data_15min['pattern'] = (
#    (data_15min['ma_uptrend'].shift(2)) &  # Two intervals ago: Uptrend
    data_15min['pct_uptrend'] &
    (data_15min['ma_uptrend'].shift(1)) &  # One interval ago: Uptrend
    (data_15min['closePrice'] < data_15min['openPrice'])  # Current interval: Downtrend
)

# --- STEP 5: Check Profitability Following the Pattern ---
# Define profit target (e.g., $10, $20, $40)
delta_price = 10  # Adjust as needed

# Calculate whether the profit target is hit in the NEXT 15-minute interval
data_15min['next_close'] = data_15min['highPrice'].shift(-1)  # Close price in the next interval
data_15min['profit_target_hit'] = (data_15min['next_close'] - data_15min['closePrice']) >= delta_price

# Filter rows where the "Up → Up → Down" pattern is detected
pattern_data = data_15min[data_15min['pattern']]

# --- STEP 6: Analyze Success Rate ---
success_rate_after_pattern = pattern_data['profit_target_hit'].mean()

# Print Results
print("=== RESULTS ===")
print(f"Number of 'Up → Up → Down' Patterns Found: {len(pattern_data)}")
print(f"Success Rate After 'Up → Up → Down' Pattern: {success_rate_after_pattern * 100:.2f}%")

# General Success Rate for Comparison
general_success_rate = data_15min['profit_target_hit'].mean()
print(f"General Success Rate (All Intervals): {general_success_rate * 100:.2f}%")

# --- OPTIONAL: Analyze Pattern Frequency ---
print(f"Total Intervals: {len(data_15min)}")
print(f"Pattern Frequency: {len(pattern_data) / len(data_15min) * 100:.2f}%")
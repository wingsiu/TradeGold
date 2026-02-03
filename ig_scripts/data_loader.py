import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime
import os
from typing import Optional

# Load environment variables from .env
load_dotenv()

# Database Configuration from .env
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

class DataLoader:
    def __init__(self):
        """
        Initialize the DataLoader. It uses the database configuration from the environment variables
        and establishes the SQLAlchemy engine.
        """
        self.engine = create_engine(
            f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
        )

    def load_data(self, table_name: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Load data from the specified table in the MySQL database using SQLAlchemy.

        Args:
        - table_name (str): The name of the table to query data from.
        - start_date (Optional[str]): Optional start date for filtering the data (format: 'YYYY-MM-DD').
        - end_date (Optional[str]): Optional end date for filtering the data (format: 'YYYY-MM-DD').

        Returns:
        - pd.DataFrame: The loaded data as a Pandas DataFrame.
        """
        # Define the base SQL query
        query = f"""
            SELECT 
                timestamp, 
                openPrice, openPrice_ask, openPrice_bid, 
                closePrice, closePrice_ask, closePrice_bid, 
                highPrice, highPrice_ask, highPrice_bid, 
                lowPrice, lowPrice_ask, lowPrice_bid, 
                lastTradedVolume 
            FROM {table_name}
        """
        conditions = []

        # Add date filtering if provided
        if start_date:
            dt = datetime.strptime(start_date, "%Y-%m-%d")
            start_timestamp = int(datetime(year=dt.year, month=dt.month, day=dt.day, hour=6, minute=0).timestamp()) * 1000
            conditions.append(f"timestamp >= '{start_timestamp}'")
        if end_date:
            dt = datetime.strptime(end_date, "%Y-%m-%d")
            end_timestamp = int(datetime(year=dt.year, month=dt.month, day=dt.day, hour=6, minute=0).timestamp()) * 1000
            conditions.append(f"timestamp <= '{end_timestamp}'")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # Execute the SQL query and load into a DataFrame
        data = pd.read_sql(query, self.engine)
        print(f"Data successfully loaded: {len(data)} rows.")
        return data

# Example usage
if __name__ == "__main__":
    # Initialize the DataLoader
    loader = DataLoader()

    # Load data from the `prices` table with optional date filters
    data = loader.load_data("gold_prices", start_date="2025-01-01", end_date="2026-01-31")
    data.to_csv('gold_prices.csv')
    # Display the first few rows of the data
    print(data.head())
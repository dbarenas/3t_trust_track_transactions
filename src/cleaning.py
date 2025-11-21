import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

def clean_data(raw_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """Cleans and preprocesses raw data."""
    if not raw_data:
        return pd.DataFrame()

    df = pd.DataFrame(raw_data)

    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Convert data types
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if 'amount' in df.columns:
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    if 'valuation_amount' in df.columns:
        df['valuation_amount'] = pd.to_numeric(df['valuation_amount'], errors='coerce')

    # Handle missing values
    if 'sender_id' in df.columns:
        df.dropna(subset=['transaction_id', 'sender_id', 'receiver_id', 'amount'], inplace=True)

    return df

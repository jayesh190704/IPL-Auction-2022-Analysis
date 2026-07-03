import sys
from pathlib import Path

# Add parent directory to path so we can import config
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import numpy as np
import logging
from config import RAW_DATA_DIR, LOG_LEVEL, LOG_FILE, AUCTION_YEAR

RAW_DATA_PATH = RAW_DATA_DIR / "ipl_2022_dataset.csv"
CLEAN_DATA_PATH = RAW_DATA_DIR / "players_clean.csv"

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def convert_price(price_str):
    """Convert price strings like '2 Cr', '40 Lakh' to numeric values"""
    if pd.isna(price_str):
        return np.nan
    price_str = str(price_str).strip()
    if price_str.lower() in ["draft pick", "retained", "unsold", ""]:
        return np.nan
    # Check if already a number
    try:
        return float(price_str) * 10000000  # if in Cr
    except ValueError:
        pass
    # Process string prices
    price_str = price_str.replace('₹', '').replace(',', '')
    if 'Cr' in price_str:
        return float(price_str.replace('Cr', '').strip()) * 10000000
    elif 'Lakh' in price_str:
        return float(price_str.replace('Lakh', '').strip()) * 100000
    else:
        try:
            return float(price_str) * 10000000  # assume Cr if no unit
        except:
            return np.nan

def main():
    logging.info("=== Starting data cleaning process ===")
    try:
        logging.info(f"Loading raw data from {RAW_DATA_PATH}")
        df = pd.read_csv(RAW_DATA_PATH)
        
        logging.info("Dropping unnecessary first column")
        df = df.drop(df.columns[0], axis=1)
        
        logging.info("Renaming columns")
        df = df.rename(columns={
            "Player": "player_name",
            "Base Price": "base_price",
            "TYPE": "role",
            "COST IN ₹ (CR.)": "sold_price",
            "Team": "team"
        })
        
        logging.info("Converting price columns")
        df["base_price"] = df["base_price"].apply(convert_price)
        df["sold_price"] = df["sold_price"].apply(lambda x: float(x) * 10000000 if pd.notna(x) else np.nan)
        
        logging.info("Adding country placeholder and auction year")
        df["country"] = np.nan
        df["auction_year"] = AUCTION_YEAR
        
        logging.info("Selecting required columns")
        df = df[["player_name", "country", "team", "role", "base_price", "sold_price", "auction_year"]]
        
        logging.info("Removing duplicates")
        df = df.drop_duplicates()
        
        logging.info("Converting data types")
        df["base_price"] = df["base_price"].astype("Int64")  # nullable integer
        df["sold_price"] = df["sold_price"].astype("Int64")
        df["auction_year"] = df["auction_year"].astype(int)
        
        logging.info(f"Saving cleaned data to {CLEAN_DATA_PATH}")
        df.to_csv(CLEAN_DATA_PATH, index=False)
        logging.info(f"Data cleaning completed! Number of records: {len(df)}")
        logging.info("=== Data cleaning process completed ===")
        
    except Exception as e:
        logging.error(f"Error during data cleaning: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()

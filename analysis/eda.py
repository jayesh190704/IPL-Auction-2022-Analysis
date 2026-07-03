import sys
from pathlib import Path

# Add parent directory to path so we can import config
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import logging
from config import PLAYERS_CLEAN_CSV, LOG_LEVEL, LOG_FILE

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def perform_eda():
    logging.info("=== Starting Exploratory Data Analysis ===")
    
    try:
        logging.info(f"Loading cleaned data from {PLAYERS_CLEAN_CSV}")
        df = pd.read_csv(PLAYERS_CLEAN_CSV)
        
        # How many players?
        total_players = len(df)
        logging.info(f"Total players: {total_players}")
        
        # How many countries? (if we had data, but let's handle it)
        countries = df['country'].dropna().nunique()
        logging.info(f"Number of countries (with data): {countries}")
        
        # Most expensive player
        expensive_player = df.loc[df['sold_price'].idxmax()] if not df['sold_price'].isna().all() else None
        if expensive_player is not None:
            logging.info(f"Most expensive player: {expensive_player['player_name']} - Rs.{expensive_player['sold_price']:,}")
        
        # Average sold price
        avg_price = df['sold_price'].mean()
        logging.info(f"Average sold price: Rs.{avg_price:,.0f}")
        
        # Median sold price
        median_price = df['sold_price'].median()
        logging.info(f"Median sold price: Rs.{median_price:,.0f}")
        
        # Highest spending team
        team_spending = df.groupby('team')['sold_price'].sum().sort_values(ascending=False)
        if not team_spending.empty:
            highest_team = team_spending.index[0]
            logging.info(f"Highest spending team: {highest_team} - Rs.{team_spending[highest_team]:,.0f}")
            
            lowest_team = team_spending.index[-1]
            logging.info(f"Lowest spending team: {lowest_team} - Rs.{team_spending[lowest_team]:,.0f}")
        
        # Number of batsmen, bowlers, etc.
        role_counts = df['role'].value_counts()
        logging.info("Players by role:")
        for role, count in role_counts.items():
            logging.info(f"  {role}: {count}")
        
        # Unsold percentage
        unsold_count = df['sold_price'].isna().sum()
        unsold_pct = (unsold_count / total_players) * 100
        logging.info(f"Unsold players: {unsold_count} ({unsold_pct:.1f}%)")
        
        logging.info("=== EDA completed successfully ===")
        return df
        
    except Exception as e:
        logging.error(f"Error during EDA: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    perform_eda()

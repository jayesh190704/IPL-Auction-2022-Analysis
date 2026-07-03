import sys
from pathlib import Path

# Add parent directory to path so we can import config
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import logging
from sqlalchemy import create_engine, text
from config import (
    PLAYERS_CLEAN_CSV, 
    DB_USER, 
    DB_PASSWORD, 
    DB_HOST, 
    DB_NAME, 
    LOG_LEVEL, 
    LOG_FILE
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def import_to_mysql():
    logging.info("=== Starting MySQL data import ===")
    
    try:
        logging.info("Connecting to MySQL database")
        # Create database engine
        engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
        
        logging.info(f"Loading cleaned data from {PLAYERS_CLEAN_CSV}")
        df = pd.read_csv(PLAYERS_CLEAN_CSV)
        
        logging.info("Importing data into 'players' table")
        df.to_sql("players", engine, if_exists="replace", index=False)
        
        # Add player_id as primary key
        logging.info("Adding player_id primary key column")
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE players ADD COLUMN player_id INT AUTO_INCREMENT PRIMARY KEY FIRST;"))
            conn.commit()
        
        logging.info("=== Data imported successfully ===")
        
    except Exception as e:
        logging.error(f"Error during import: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    import_to_mysql()

from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent
RAW_DATA_DIR = BASE_DIR / "raw_data"
PROCESSED_DATA_DIR = BASE_DIR / "processed_data"
IMAGES_DIR = BASE_DIR / "images"
SCRAPER_DIR = BASE_DIR / "scraper"
SQL_DIR = BASE_DIR / "sql"

# Create directories if they don't exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, IMAGES_DIR]:
    directory.mkdir(exist_ok=True)

# IPL Auction URL
AUCTION_URL = "https://www.iplt20.com/auction/2022"
AUCTION_YEAR = 2022
AUCTION_DATE = "2022-02-12"

# File names
PLAYERS_RAW_CSV = RAW_DATA_DIR / "players_raw.csv"
PLAYERS_CLEAN_CSV = RAW_DATA_DIR / "players_clean.csv"

# Database configuration
DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_NAME = "ipl_auction"

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FILE = BASE_DIR / "app.log"

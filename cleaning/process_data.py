import csv
from pathlib import Path
import pandas as pd
from datetime import date

AUCTION_YEAR = 2022
AUCTION_DATE = date(2022, 2, 12)
OUTPUT_FILE = Path(__file__).resolve().parents[1] / "raw_data" / "players_raw.csv"

# Load both datasets
df1 = pd.read_csv(Path(__file__).resolve().parents[1] / "raw_data" / "players_raw.csv")
df2 = pd.read_csv(Path(__file__).resolve().parents[1] / "raw_data" / "ipl_2022_dataset.csv")

# Clean up column names
df1 = df1.rename(columns={
    "Teams": "Team",
    "Player_Name": "Player Name",
    "Nationality": "Country",
    "Type": "Role",
    "Sold_Price": "Sold Price"
})

# Add missing columns
df1["Auction Year"] = AUCTION_YEAR
df1["Auction Date"] = AUCTION_DATE.isoformat()
df1["Status"] = "Sold"

# Add Base Price from df2
df2 = df2.rename(columns={"Player": "Player Name"})
df1 = df1.merge(df2[["Player Name", "Base Price"]], on="Player Name", how="left")

# Reorder columns to match OUTPUT_COLUMNS from scraper.py
OUTPUT_COLUMNS = [
    "Auction Year",
    "Auction Date",
    "Status",
    "Team",
    "Team Slug",
    "Sr No",
    "Player Name",
    "Player Profile URL",
    "Search URL",
    "Country",
    "Role",
    "Specialization",
    "Base Price",
    "Sold Price",
    "Capped Status",
    "Is Overseas",
    "IPL Debut",
    "Date of Birth",
    "Age",
    "Matches",
    "Batting Style",
    "Bowling Style",
    "About",
    "Auction Source URL"
]

# Add any missing columns
for col in OUTPUT_COLUMNS:
    if col not in df1.columns:
        df1[col] = ""

# Set Team Slug
df1["Team Slug"] = df1["Team"].str.lower().str.replace(" ", "-")

# Set Is Overseas
df1["Is Overseas"] = df1["Country"].apply(lambda x: "No" if x == "Indian" else "Yes")

# Set Auction Source URL
df1["Auction Source URL"] = f"https://www.iplt20.com/auction/{AUCTION_YEAR}"

# Save the final dataset
df1[OUTPUT_COLUMNS].to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
print(f"Processed data saved to {OUTPUT_FILE}")

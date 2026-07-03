import sys
from pathlib import Path

# Add parent directory to path so we can import config
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import matplotlib.pyplot as plt
import logging
from config import PLAYERS_CLEAN_CSV, IMAGES_DIR, LOG_LEVEL, LOG_FILE

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# Set matplotlib style
plt.style.use('seaborn-v0_8')

def create_visualizations():
    logging.info("=== Starting visualization creation ===")
    
    try:
        df = pd.read_csv(PLAYERS_CLEAN_CSV)
        
        # 1. Top 10 Sold Players - Bar Chart
        logging.info("Creating top 10 sold players bar chart")
        top10 = df.sort_values('sold_price', ascending=False).head(10).dropna(subset=['sold_price'])
        plt.figure(figsize=(12, 8))
        bars = plt.barh(top10['player_name'], top10['sold_price']/10000000, color='#1f77b4')
        plt.xlabel('Sold Price (₹ Crore)')
        plt.ylabel('Player Name')
        plt.title('Top 10 Most Expensive Players - IPL 2022 Auction')
        plt.gca().invert_yaxis()  # To have highest at top
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 0.1, bar.get_y() + bar.get_height()/2,
                    f'{width:.1f}', va='center')
        plt.tight_layout()
        plt.savefig(IMAGES_DIR / 'top10_players.png', dpi=300)
        plt.close()
        
        # 2. Team Spending - Bar Chart
        logging.info("Creating team spending bar chart")
        team_spending = df.groupby('team')['sold_price'].sum().sort_values(ascending=True)
        plt.figure(figsize=(12, 8))
        bars = plt.barh(team_spending.index, team_spending/10000000, color='#2ca02c')
        plt.xlabel('Total Spending (₹ Crore)')
        plt.ylabel('Team')
        plt.title('Total Spending by Team - IPL 2022 Auction')
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                    f'{width:.1f}', va='center')
        plt.tight_layout()
        plt.savefig(IMAGES_DIR / 'team_spending.png', dpi=300)
        plt.close()
        
        # 3. Players by Country - Pie Chart (we don't have country data yet, so let's use role as a placeholder or skip? Wait, let's make one using role or we can use team. Alternatively, let's check if we have any country data. If not, let's make role distribution.)
        # Since we don't have country data, let's make Players by Role pie chart
        logging.info("Creating players by role pie chart")
        role_counts = df['role'].value_counts()
        plt.figure(figsize=(10, 10))
        wedges, texts, autotexts = plt.pie(role_counts, labels=role_counts.index, autopct='%1.1f%%', colors=plt.cm.Paired.colors)
        plt.title('Distribution of Players by Role - IPL 2022 Auction')
        plt.tight_layout()
        plt.savefig(IMAGES_DIR / 'role_distribution.png', dpi=300)
        plt.close()
        
        # 4. Price Distribution - Histogram
        logging.info("Creating price distribution histogram")
        plt.figure(figsize=(12, 6))
        sold_prices = df['sold_price'].dropna()
        plt.hist(sold_prices/10000000, bins=20, color='#ff7f0e', edgecolor='black')
        plt.xlabel('Sold Price (₹ Crore)')
        plt.ylabel('Number of Players')
        plt.title('Distribution of Auction Prices - IPL 2022')
        plt.tight_layout()
        plt.savefig(IMAGES_DIR / 'price_distribution.png', dpi=300)
        plt.close()
        
        # 5. Sold Price Outliers - Box Plot
        logging.info("Creating sold price box plot")
        plt.figure(figsize=(12, 6))
        plt.boxplot(sold_prices/10000000, vert=False)
        plt.xlabel('Sold Price (₹ Crore)')
        plt.title('Box Plot of Auction Prices - IPL 2022')
        plt.tight_layout()
        plt.savefig(IMAGES_DIR / 'price_boxplot.png', dpi=300)
        plt.close()
        
        logging.info(f"All visualizations saved to {IMAGES_DIR}")
        logging.info("=== Visualization creation completed ===")
        
    except Exception as e:
        logging.error(f"Error creating visualizations: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    create_visualizations()

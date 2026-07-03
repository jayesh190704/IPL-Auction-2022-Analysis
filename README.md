# IPL Auction Analysis 2022

A comprehensive data analysis project of the Indian Premier League (IPL) 2022 player auction, including web scraping, data cleaning, SQL analysis, Python EDA, and visualizations.

---

## Project Overview

This project analyzes the IPL 2022 player auction to gain insights into:
- Player auction prices
- Team spending patterns
- Distribution of player roles
- Most expensive players
- Unsold players

---

## Dataset Source

The dataset was collected from publicly available IPL auction data. The data includes:
- Player names
- Nationality
- Role
- Base price
- Sold price
- Teams

---

## Technologies Used

- **Python 3.14**: Core programming language
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Data visualization
- **SQLAlchemy**: Database connection
- **PyMySQL**: MySQL driver
- **Selenium**: (Optional) Web scraping
- **MySQL**: Database management system
- **Git**: Version control

---

## Folder Structure

```
IPL-Auction-Analysis/
├── analysis/           # Exploratory Data Analysis (EDA) scripts
│   └── eda.py
├── cleaning/           # Data cleaning scripts
│   ├── clean_data.py
│   └── process_data.py
├── images/             # Visualization outputs
├── raw_data/           # Raw and cleaned datasets
│   ├── ipl_2022_dataset.csv
│   ├── players_clean.csv
│   └── players_raw.csv
├── scraper/            # Web scraping scripts
│   └── scraper.py
├── sql/                # SQL schema and queries
│   ├── analysis.sql
│   ├── import_data.py
│   └── schema.sql
├── visualization/      # Data visualization scripts
│   └── charts.py
├── .gitignore
├── config.py           # Centralized configuration
├── requirements.txt    # Dependencies
└── README.md           # Project documentation
```

---

## Workflow Diagram

```
1. Raw Data Collection
       ↓
2. Data Cleaning
       ↓
3. Exploratory Data Analysis (EDA)
       ↓
4. Data Visualization
       ↓
5. SQL Database Import
       ↓
6. SQL Analysis
```

---

## SQL Queries

The `sql/analysis.sql` file contains all SQL queries used for analysis:

1. **Highest Sold Player**:
   ```sql
   SELECT * FROM players ORDER BY sold_price DESC LIMIT 1;
   ```

2. **Average Team Spending**:
   ```sql
   SELECT team, AVG(sold_price) AS average_spending FROM players GROUP BY team;
   ```

3. **Top 10 Expensive Players**:
   ```sql
   SELECT player_name, sold_price FROM players ORDER BY sold_price DESC LIMIT 10;
   ```

4. **Players by Country**:
   ```sql
   SELECT country, COUNT(*) AS count FROM players WHERE country IS NOT NULL GROUP BY country;
   ```

5. **Unsold Players**:
   ```sql
   SELECT * FROM players WHERE sold_price IS NULL;
   ```

6. **Total Spending by Team**:
   ```sql
   SELECT team, SUM(sold_price) AS total_spending FROM players GROUP BY team ORDER BY total_spending DESC;
   ```

---

## Visualizations

All visualizations are saved in the `images/` directory:

1. **Top 10 Sold Players** (`images/top10_players.png`)
   - Horizontal bar chart showing the 10 most expensive players
2. **Team Spending** (`images/team_spending.png`)
   - Horizontal bar chart of total spending per team
3. **Player Roles** (`images/role_distribution.png`)
   - Pie chart of player role distribution
4. **Price Distribution** (`images/price_distribution.png`)
   - Histogram of sold prices
5. **Price Box Plot** (`images/price_boxplot.png`)
   - Box plot showing price distribution and outliers

---

## Results

Key insights from the analysis:

1. **Total Players**: 632 players were part of the auction
2. **Most Expensive Player**: KL Rahul (Rs. 170,000,000)
3. **Average Sold Price**: Rs. 36,957,806
4. **Median Sold Price**: Rs. 19,000,000
5. **Highest Spending Team**: Mumbai Indians (Rs. 899,000,000)
6. **Player Roles**:
   - All-rounders: 241
   - Bowlers: 215
   - Batters: 112
   - Wicket-keepers: 64
7. **Unsold Players**: 395 (62.5%)

---

## Challenges

1. **Unicode Encoding**: Handling currency symbols in logs
2. **Database Setup**: Configuring MySQL connection
3. **Data Cleaning**: Converting price formats (Cr, Lakh) to numeric
4. **Project Structure**: Organizing files for professional presentation

---

## Future Improvements

1. Add country data from additional sources
2. Include more detailed player stats
3. Create interactive visualizations with Plotly
4. Add a web dashboard for exploring the data
5. Expand to multiple IPL seasons for trend analysis
6. Add unit tests for all scripts
7. Implement CI/CD pipeline

---

## Screenshots

*(Add screenshots of visualizations here)*

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd IPL-Auction-Analysis
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up MySQL (optional):
   - Install MySQL server
   - Create a database (e.g., `ipl_auction`)
   - Update database credentials in `config.py`

---

## Usage

### 1. Data Cleaning
```bash
python cleaning/clean_data.py
```

### 2. Exploratory Data Analysis
```bash
python analysis/eda.py
```

### 3. Create Visualizations
```bash
python visualization/charts.py
```

### 4. Import Data to MySQL (Optional)
```bash
python sql/import_data.py
```

### 5. SQL Analysis
Execute queries from `sql/analysis.sql` in your MySQL client.

---

## License

[Your License Here]

---

## Contributors

[Your Name]

---

## Acknowledgments

- IPL official website for data
- All open-source contributors to the libraries used

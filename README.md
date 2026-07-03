# 🏏 IPL Auction 2026 Web Scraper & Data Analysis

> A Python-based web scraping project that extracts IPL Auction 2026 player information from the official IPL website, cleans the data, and exports it for further analysis using Pandas and SQL.

---

## 📌 Project Overview

The **IPL Auction 2026 Web Scraper** is a beginner-friendly data collection project built using Python. It demonstrates the complete workflow of acquiring data from a website, parsing HTML content, organizing the extracted information into structured datasets, and preparing it for data analysis.

This project was created to strengthen practical skills in:

* Web Scraping
* Data Collection
* Data Cleaning
* Data Analysis
* Python Programming
* SQL Integration

---

## 🎯 Project Objectives

* Scrape IPL Auction player information from the official IPL website.
* Extract structured player data.
* Store the collected information in CSV format.
* Prepare the dataset for SQL and Python analysis.
* Demonstrate an end-to-end data collection workflow.

---

## 🛠 Tech Stack

| Category               | Technologies             |
| ---------------------- | ------------------------ |
| Language               | Python 3                 |
| Web Scraping           | Requests, BeautifulSoup4 |
| Data Processing        | Pandas, NumPy            |
| Notebook               | Jupyter Notebook         |
| Database (Future)      | MySQL                    |
| Visualization (Future) | Matplotlib, Plotly       |

---

## 📂 Project Structure

```text
IPL-Auction-Web-Scraper/
│
├── ipl-auction-web-scraper.ipynb
├── requirements.txt
├── README.md
├── raw_data/
│   └── players_raw.csv
├── processed_data/
│   └── players_clean.csv
├── sql/
│   ├── schema.sql
│   └── analysis.sql
├── images/
└── .gitignore
```

---

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/IPL-Auction-Web-Scraper.git
```

Move into the project directory:

```bash
cd IPL-Auction-Web-Scraper
```

Install all required libraries:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

Launch Jupyter Notebook:

```bash
jupyter notebook
```

Open:

```text
ipl-auction-web-scraper.ipynb
```

Run all notebook cells sequentially.

---

## 🔄 Project Workflow

```text
Official IPL Website
        │
        ▼
HTTP Request
        │
        ▼
HTML Parsing (BeautifulSoup)
        │
        ▼
Extract Player Information
        │
        ▼
Create Pandas DataFrame
        │
        ▼
Clean & Process Data
        │
        ▼
Export CSV
        │
        ▼
SQL Analysis (Future)
        │
        ▼
Visualization Dashboard (Future)
```

---

## 📊 Features

* Fetch webpage content using Requests
* Parse HTML using BeautifulSoup
* Extract structured auction data
* Convert extracted data into a Pandas DataFrame
* Export results to CSV
* Beginner-friendly project structure
* Easy to extend for advanced analytics

---

## 📋 Expected Dataset

The scraper aims to collect information such as:

| Column         |
| -------------- |
| Player Name    |
| Country        |
| Role           |
| Base Price     |
| Sold Price     |
| Team           |
| Auction Status |
| Auction Year   |

---

## 📈 Future Analysis

After collecting the data, it can be used to answer questions like:

* Which player received the highest bid?
* Which team spent the most money?
* Which country had the most players?
* Average player price.
* Team-wise spending.
* Unsold players.
* Role-wise distribution.
* Most expensive overseas players.

---

## 📊 Future Visualizations

Planned visualizations include:

* Top 10 Highest Sold Players
* Team Spending Analysis
* Country-wise Player Distribution
* Auction Price Distribution
* Role Distribution
* Base Price vs Sold Price
* Sold vs Unsold Players

---

## 🗄 SQL Analysis (Planned)

Example SQL queries:

* Highest sold player
* Team-wise expenditure
* Country-wise player count
* Unsold players
* Average sold price
* Top 10 expensive players

---

## 📚 Python Libraries Used

```python
requests
beautifulsoup4
pandas
numpy
```

Install using:

```bash
pip install requests beautifulsoup4 pandas numpy
```

---

## 💡 Skills Demonstrated

* Python Programming
* Web Scraping
* HTML Parsing
* Data Collection
* Data Cleaning
* Data Manipulation
* CSV Export
* Pandas
* Jupyter Notebook
* Problem Solving

---

## ⚠️ Current Limitation

The official IPL Auction website loads most of its data dynamically using **JavaScript**.

Since this project currently uses **Requests + BeautifulSoup**, dynamically rendered content may not be available in the downloaded HTML.

As a result, some auction tables may not be extracted successfully.

### Planned Solution

The next version of this project will use:

* Selenium
* ChromeDriver
* Explicit Waits
* Dynamic Page Handling

to scrape JavaScript-rendered content accurately.

---

## 🚀 Future Improvements

* Selenium-based scraping
* Automatic data cleaning
* MySQL database integration
* SQL analytics
* Interactive dashboard
* Scheduled data collection
* Logging system
* Exception handling
* Modular Python scripts
* Power BI dashboard
* Automated report generation

---

## 📸 Screenshots

Add screenshots here after running the project.

Example:

```
images/
├── scraper_output.png
├── dataframe_preview.png
├── csv_output.png
├── sql_queries.png
└── charts.png
```

---

## 🤝 Contributing

Contributions are welcome.

If you'd like to improve this project:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Jayesh Marathe**

Computer Science Student

Python • SQL • Data Analytics • Data Science

GitHub: https://github.com/jayesh190704

LinkedIn: https://www.linkedin.com/in/jayeshmarathe53

---

## ⭐ If you found this project useful

Please consider giving it a **Star ⭐** on GitHub.

It helps support the project and motivates future improvements.

---

## 📬 Contact

If you have any suggestions or feedback, feel free to connect through GitHub or LinkedIn.

Happy Coding! 🚀

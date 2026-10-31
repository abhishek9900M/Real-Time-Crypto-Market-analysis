# Real-Time Cryptocurrency Market Analysis & Automation

An end-to-end data engineering and analytics project that collects cryptocurrency market data from the CoinGecko API, processes it using Python, stores the latest market snapshot in Microsoft SQL Server, and visualizes market insights using Power BI.

The project also automates Excel report generation and email delivery using Python and Windows Task Scheduler.

## Project Overview

This project automates cryptocurrency market data extraction, transformation, storage, reporting, and visualization.

Python retrieves cryptocurrency market data from CoinGecko, processes multiple API pages, cleans the dataset, and inserts the latest snapshot into SQL Server.

Power BI connects to SQL Server using DirectQuery to visualize market performance. Python also generates an Excel report containing the top 20 cryptocurrencies by market capitalization and sends it through Gmail automatically.

## Architecture

```text
             CoinGecko API
                   |
                   v
          Python Data Extraction
                   |
                   v
         Data Cleaning & Processing
                   |
                   v
              SQL Server
                   |
             +-----+------+
             |            |
             v            v
          Power BI     Excel Report
         DirectQuery   Top 20 Coins
                          |
                          v
                    Gmail Delivery
                          |
                          v
                   Task Scheduler
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data extraction and automation |
| CoinGecko API | Cryptocurrency market data |
| Pandas | Data cleaning and transformation |
| Requests | API integration |
| SQL Server | Database storage |
| PyODBC | Python–SQL Server connectivity |
| Power BI | Interactive dashboard |
| Excel / OpenPyXL | Report generation |
| SMTP / Gmail | Automated email delivery |
| Windows Task Scheduler | Scheduled execution |

## Data Collection

The project uses the CoinGecko `/coins/markets` endpoint.

**API configuration:**
- Currency: USD
- Sorting: Market capitalization descending
- Pages: 1–3
- Records per page: 250
- Sparkline: Disabled

The pipeline collects cryptocurrency information such as:

- Cryptocurrency ID, name, and symbol
- Current price
- Market capitalization and market cap rank
- Total trading volume
- 24-hour price change
- Circulating, total, and maximum supply
- Last updated timestamp
- Data collection timestamp

## Data Processing

Python and Pandas are used to:

1. Fetch multiple pages from the API.
2. Combine API responses into one dataset.
3. Remove unnecessary columns.
4. Handle missing and null values.
5. Convert data types for SQL Server compatibility.
6. Round cryptocurrency prices to two decimal places.
7. Add a collection timestamp.
8. Prepare clean records for database insertion.

## Database Management

**Database:** `realtimecryptodata`

**Table:** `dbo.cryptocaol`

**Database engine:** Microsoft SQL Server

The pipeline follows a snapshot-based storage approach:

1. Fetch the latest market data.
2. Validate and process the API response.
3. Remove the previous snapshot after successful data retrieval and validation.
4. Insert the latest cryptocurrency records.

This maintains the latest market snapshot without accumulating duplicate records from every refresh.

## Power BI Dashboard

Power BI connects to SQL Server using DirectQuery.

Dashboard analysis includes:

- Total cryptocurrencies tracked
- Current cryptocurrency prices
- Market capitalization
- Trading volume
- Cryptocurrency market rankings
- 24-hour price changes
- Market performance comparisons

## Automated Excel Reporting

Python generates an Excel report from the latest cryptocurrency dataset.

**Reporting workflow:**

1. Read the latest Excel market data.
2. Select the first 20 records.
3. Generate `top_20_market_data.xlsx`.
4. Attach the report to an email.
5. Send the report through Gmail SMTP.

Since the API data is sorted by market capitalization in descending order, the first 20 records represent the top 20 cryptocurrencies by market capitalization.

## Email Automation

The project uses Gmail SMTP with an App Password for automated email delivery.

Configuration is maintained in a local `.env` file:

```env
GMAIL_ADDRESS=your_email@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
REPORT_TO_EMAIL=recipient@gmail.com
```

Never upload `.env` or actual credentials to GitHub.

## Scheduled Automation

Windows Task Scheduler executes the main Python pipeline automatically.

**Configured schedule:**

- 9:00 AM
- 3:00 PM
- 9:00 PM

Each scheduled execution runs the data pipeline, updates SQL Server and Excel, generates the Top 20 report, and sends the email.

The computer must be powered on for scheduled execution.

## Project Structure

```text
Real-Time-Crypto-Market-analysis/
│
├── Coin_API_Main.py
├── Data_pipeline_insertion2.py
├── SQL_Connect.py
├── email_report.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── Crypto Market Dashboard.pbip
├── Screenshot 2026-10-28 234803.png
│
└── .env                 (local only, not uploaded)
```

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/abhishek9900M/Real-Time-Crypto-Market-analysis.git

cd Real-Time-Crypto-Market-analysis
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure SQL Server

Configure your SQL Server instance, database name, authentication, and ODBC Driver 18 connection settings in the database connection script.

Create the required database and table before running the pipeline.

### 5. Configure Gmail

Create a local `.env` file containing the required Gmail settings. Use a Gmail App Password rather than your normal account password.

### 6. Run the pipeline

```bash
python Coin_API_Main.py
```

### 7. Open the Power BI dashboard

Open `Crypto Market Dashboard.pbip` in Power BI Desktop and configure the SQL Server connection for your environment.

## Key Features

- CoinGecko API integration
- Multi-page cryptocurrency data extraction
- Data cleaning and transformation using Pandas
- SQL Server snapshot-based storage
- Duplicate prevention through snapshot replacement
- Power BI DirectQuery integration
- Automated Excel report generation
- Top 20 cryptocurrency reporting
- Gmail SMTP email automation
- Windows Task Scheduler integration
- Git and GitHub version control

## Future Improvements

- WhatsApp Cloud API report delivery
- Historical cryptocurrency price tracking
- Advanced market trend analysis
- Improved pipeline logging and error monitoring
- Automated pipeline failure notifications

## Project Type

**End-to-End Data Engineering & Analytics Project**

Python | REST API | Pandas | SQL Server | Power BI | Excel Automation | SMTP | Task Scheduler

## Data Source

[CoinGecko API](https://www.coingecko.com/en/api)

*Disclaimer: This project is developed for educational and analytical purposes. Cryptocurrency market data changes frequently and should not be considered financial advice.*

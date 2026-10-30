# Real-Time Cryptocurrency Market Analysis and  Dashboard

An end-to-end data engineering and analytics project that collects live cryptocurrency market data using the CoinGecko API, processes it with Python, stores market snapshots in Microsoft SQL Server, and visualizes market trends through Power BI.

## Project Overview

The project automates cryptocurrency market data collection and creates a structured database for real-time market analysis.

Python fetches cryptocurrency data from the CoinGecko API, processes and cleans the response, and stores the latest market snapshot in SQL Server. Power BI connects to the database using DirectQuery to visualize cryptocurrency market performance.

## Project Objectives

- Fetch cryptocurrency market data using the CoinGecko API.
- Collect data for multiple cryptocurrencies.
- Process and clean API responses using Python.
- Store cryptocurrency market snapshots in SQL Server.
- Avoid duplicate records during snapshot updates.
- Visualize market performance using Power BI.
- Build an automated data pipeline.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | API integration and data processing |
| CoinGecko API | Cryptocurrency market data source |
| Pandas | Data cleaning and transformation |
| Requests | API requests |
| Microsoft SQL Server | Database storage |
| Power BI | Interactive dashboard |
| ODBC Driver 18 | Python–SQL Server connectivity |

## Data Pipeline Architecture

```text
CoinGecko API
      |
      v
Python API Integration
      |
      v
Data Extraction
      |
      v
Data Cleaning & Transformation
      |
      v
SQL Server Database
      |
      v
Power BI DirectQuery
      |
      v
Interactive Crypto Dashboard
```

## Data Collection

The project uses the CoinGecko `/coins/markets` API endpoint to collect cryptocurrency market information.

### Data Fields

- Cryptocurrency ID
- Cryptocurrency Name
- Symbol
- Current Price (USD)
- Market Capitalization
- Market Cap Rank
- Total Volume
- 24-Hour Price Change
- 24-Hour Price Change Percentage
- Circulating Supply
- Total Supply
- Maximum Supply
- Last Updated
- Collected At

The API data is collected across multiple pages to retrieve a larger set of cryptocurrencies.

## Data Processing

Python and Pandas are used to:

- Fetch API responses.
- Combine multiple API pages.
- Remove unnecessary columns.
- Handle missing and null values.
- Convert data types for SQL Server compatibility.
- Round cryptocurrency prices to two decimal places.
- Add a collection timestamp.
- Prepare clean data for database insertion.

## Database Management

**Database:** `realtimecryptodata`

**Table:** `dbo.cryptocaol`

**Database:** Microsoft SQL Server

The project follows a snapshot-based data storage approach:

1. Fetch the latest cryptocurrency market data.
2. Process and validate the dataset.
3. Remove the previous snapshot only after successful data retrieval and validation.
4. Insert the latest snapshot into SQL Server.

This approach keeps the database focused on the latest market data rather than maintaining duplicate records from every refresh.

## Power BI Dashboard

Power BI connects to SQL Server using DirectQuery to visualize the latest stored cryptocurrency market data.

### Dashboard Analysis

- Total cryptocurrencies tracked
- Current cryptocurrency prices
- Market capitalization
- Trading volume
- Cryptocurrency market rankings
- Price change percentage
- Market performance comparison

## Project Structure

```text
Crypto-Real-Time-Dashboard/
│
├── Coin_API_Main.py
├── SQL_Connect.py
├── test_insert.py
├── requirements.txt
├── README.md
│
└── PowerBI/
    └── Crypto_Dashboard.pbix
```

*Adjust the filenames and folders to match your actual GitHub repository.*

## Installation & Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Crypto-Real-Time-Dashboard
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure SQL Server

Update the database connection settings in your Python connection script.

Configure:
- SQL Server instance
- Database name
- ODBC Driver
- Authentication settings

Do not upload passwords or private credentials to GitHub.

### 4. Run the Python Script

```bash
python Coin_API_Main.py
```

### 5. Open Power BI

Open the Power BI dashboard file and configure its SQL Server connection to view cryptocurrency market analytics.

## Key Features

- API-based cryptocurrency data extraction.
- Automated multi-page data collection.
- Data cleaning and transformation using Pandas.
- SQL Server database integration.
- Snapshot-based data replacement.
- Power BI DirectQuery integration.
- Interactive cryptocurrency market visualization.

## Project Type

**End-to-End Data Engineering & Analytics Project**

Python | REST API | Pandas | SQL Server | Power BI

## Data Source

CoinGecko API: https://www.coingecko.com/en/api

**Disclaimer:** This project is developed for educational and analytical purposes. Cryptocurrency market data is subject to change and should not be considered financial advice.

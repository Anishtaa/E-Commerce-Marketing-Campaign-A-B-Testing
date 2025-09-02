# Movate E-commerce Analysis Project

## Project Overview
This project analyzes e-commerce campaign data and provides insights through interactive dashboards. It focuses on tracking marketing campaign performance, site activity, and overall transactional trends. Two dashboards are included: one developed in **Python** and another that uses **SQL** queries.

## Features

### Python Dashboard (`dashboard.py`)
- Built with **Dash** and **Plotly** for interactive visualization.
- Displays insights from marketing campaign and site data.
- Filterable by campaign, date, and other parameters.
- Uses cleaned CSV data (`cleaned_campaign.csv`) for analysis.

### SQL Dashboard (`dashboard_sql.py`)
- Uses **SQLite** databases (`campaign.db` and `marketing_campaign.db`) for analysis.
- Provides raw data insights and summaries via SQL queries.
- Supports aggregations like campaign performance metrics and user engagement.

### Scripts
- `01_data_preprocessing.py`: Cleans and prepares raw data for analysis.
- `02_eda.py`: Performs exploratory data analysis and generates visual insights.

## Folder Structure
E-COMMERCE CAMPAIGN ANALYSIS/
│
├── dashboards/
│ ├── dashboard.py
│ └── dashboard_sql.py
│
├── data/
│ ├── campaign.db
│ ├── marketing_campaign.db
│ ├── marketing_campaign.csv
│ └── cleaned_campaign.csv
│
├── scripts/
│ ├── 01_data_preprocessing.py
│ └── 02_eda.py
│
├── README.md
└── requirements.txt


## Installation & Setup

1. **Clone the repository**
```bash
git clone <repo-url>
cd E-COMMERCE_CAMPAIGN_ANALYSIS

pip install -r requirements.txt

--Run the Python dashboard
    python dashboards/dashboard.py

--SQL Dashboard
    The SQL dashboard uses SQLite databases in the data/ folder.
    Open dashboards/dashboard_sql.py and run to visualize insights.
  
-- Tech Stack --

Python Dashboard: Python, Dash, Plotly, Pandas

SQL Dashboard: SQLite

Data: CSV and SQLite databases

Visualization: Interactive charts, tables, and filters

// Purpose //

The project helps analyze e-commerce campaigns, track marketing performance, and extract actionable insights to optimize business decisions.
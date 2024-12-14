[
![freepik__candid-image-photography-natural-textures-highly-r__1362](https://github.com/user-attachments/assets/4a638558-ce21-429b-b4db-a789c327d49d)
](url)
# Data Warehouse Dashboard

The **Data Warehouse Dashboard** is a powerful data analytics platform built with **Django** and **SQLite**, designed to provide insightful visualizations of various data aspects, such as transactions, charity donations, user demographics, and service charges. The dashboard enables users to easily analyze and visualize key metrics through a wide array of chart types, including bar charts, pie charts, line charts, and heatmaps.
![Screenshot 2024-12-14 at 14-37-57 Data Warehouse - بحث Google](https://github.com/user-attachments/assets/bcabfff4-435f-4d43-a38c-a892817ab940)

## Features

- **ETL Process**: Initiates an Extract, Transform, Load (ETL) process to efficiently load data into the database for further analysis.
- **Unified Transaction Insights**: Visualizes transaction types, monthly trends, active vs. inactive user statuses, and transaction volume over time.
- **Donation Analysis**: Tracks and visualizes donation trends, charity categories, and total donation amounts for each charity.
- **User Demographics**: Provides demographic analysis based on user age groups, regions, and credit usage, along with a heatmap of transaction volume.
- **Service Charges Overview**: Offers detailed insights into total service charges, average charge per user, and charges segmented by type and category.
- **Interactive Visualizations**: Utilizes diverse chart types (e.g., bar, pie, line, scatter) for dynamic and interactive data exploration.

## Tech Stack

- **Backend**: Python 3.x, Django, SQLite
- **Frontend**: HTML, CSS, JavaScript (for dynamic chart rendering via libraries like Chart.js)
- **ETL Process**: Python (for handling the ETL operations)
- **Database**: SQLite (lightweight, serverless database for efficient data storage)

## Setup Instructions

To set up and run the **Data Warehouse Dashboard** locally, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Mohamedosama-dev/ETL_Data_Warehouse_.git
    cd etl_project
    ```

2. **Create a virtual environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate  
    ```

3. **Install project dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Run database migrations** to set up the necessary tables:

    ```bash
    python manage.py migrate
    ```

5. **Start the development server**:

    ```bash
    python manage.py runserver
    ```

6. **Access the dashboard**: Open your browser and navigate to `http://127.0.0.1:8000/`.

## How the Application Works

### ETL Process
The **ETL** process is triggered from the dashboard by accessing the `/trigger_etl/` route. The script performs the extraction, transformation, and loading of data into the SQLite database, preparing the dataset for analysis and visualization.

### Data Visualizations
Data is retrieved from the SQLite database using optimized SQL queries and presented via JavaScript-powered visualizations (Chart.js). The application features multiple data aggregation routes to handle the visualization of various data insights:

- **Transaction Insights**: Displays transaction types, trends over time, and the comparison of active vs. inactive users.
- **Donation Analytics**: Provides a breakdown of donations, charity categories, and donation totals per charity.
- **User Demographics**: Offers detailed insights into user segments based on age, region, and credit usage.
- **Service Charges Overview**: Analyzes the total and category-based service charges across the platform.

### Database Schema
The application utilizes a series of key models within the database:

- **TransactionFact**: Stores detailed information about each transaction, including type, amount, and date.
- **DateDimension**: Holds time-related data, such as year, month, and day, for efficient querying and analysis.
- **CharityDimension**: Contains information about the various charities involved in donation activities.
- **ServiceDimension**: Stores data related to different services offered by the platform.
- **UserDemographicsDimension**: Holds demographic data such as user age groups, regions, and credit history.
- **TransactionTypeDimension**: Captures different transaction types (e.g., deposit, withdrawal, transfer).

## Data Sources

- **Transaction Data**:Information related to transaction amounts, types, dates, and involved services.
- **Charity Data**: Details on charity donations and associated categories.
- **User Data**: Demographic data including age group, region, and credit usage.
- **Service Data**: Data on various services offered, including service charges and category breakdowns.

# Dashboard Screenshots

## Overview
This document showcases various key dashboards and features from the transaction analytics application. Each section provides a brief description alongside a screenshot to highlight the functionality and design.

---

### 1. **User Demographics Dashboard**
This dashboard provides insights into user demographics, displaying key data on user categories and trends.

![User Demographics Dashboard](https://github.com/user-attachments/assets/2b73515e-b32b-44b7-aec9-ed10bf47ceb5)

---

### 2. **Service Charges Overview**
This section outlines the details of service charges incurred, categorized by transaction type and volume.

![Screenshot 2024-12-14 at 15-07-20 Service Charges Overview](https://github.com/user-attachments/assets/b1296f99-3e8d-4cfd-aba2-fdf717d1e9d9)

---

### 3. **Charity Charges Overview**
Analyze the distribution of charity-related charges, providing transparency and insights into donation patterns.

![Screenshot 2024-12-14 at 15-12-45 Donation Analysis](https://github.com/user-attachments/assets/62baa6a9-e289-4523-985a-abde182e7acc)

---

### 4. **Transaction Dashboard**
The transaction analytics dashboard offers a comprehensive view of transactions, including volume, types, and trends over time.

![Screenshot 2024-12-14 at 15-19-33 Transaction Analytics](https://github.com/user-attachments/assets/5ef06164-9694-49b9-97c0-7ba648bde327)

---

### Notes
- These dashboards are designed to provide actionable insights for stakeholders.
- Data visualizations are rendered using Chart.js and incorporate a clean, professional UI for ease of interpretation.

Feel free to explore each section to understand the application's capabilities!

## Acknowledgments

- **Chart.js**: A popular JavaScript library for creating interactive charts and visualizations.
- **SQLite**: A lightweight, serverless database engine used for data storage.
- **Django**: A high-level Python framework used to build the backend of the application.
- **Python**: Used to implement the ETL process and backend functionality.
- **Open Source Community**: For contributing valuable libraries and resources that helped in building this project.


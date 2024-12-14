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
    git clone https://github.com/yourusername/data-warehouse-dashboard.git
    cd data-warehouse-dashboard
    ```

2. **Create a virtual environment (recommended)**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
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

- **Transaction Data**:
   Information related to transaction amounts, types, dates, and involved services.
- **Charity Data**: Details on charity donations and associated categories.
- **User Data**: Demographic data including age group, region, and credit usage.
- **Service Data**: Data on various services offered, including service charges and category breakdowns.

## Screenshots




## Acknowledgments

- **Chart.js**: A popular JavaScript library for creating interactive charts and visualizations.
- **SQLite**: A lightweight, serverless database engine used for data storage.
- **Django**: A high-level Python framework used to build the backend of the application.
- **Python**: Used to implement the ETL process and backend functionality.
- **Open Source Community**: For contributing valuable libraries and resources that helped in building this project.


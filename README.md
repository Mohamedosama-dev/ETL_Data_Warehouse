# Data Warehouse Dashboard

A comprehensive data analytics dashboard built with Django and SQLite that provides insights into various aspects of transactions, charity donations, user demographics, and service charges. The project allows users to visualize data through different types of charts, such as bar charts, pie charts, line charts, and heatmaps.

## Features

- **ETL Process**: Triggers an ETL process that extracts, transforms, and loads data into the database.
- **Unified Charts**: Provides a unified view of transaction types, monthly transactions, active vs. inactive users, and transaction volume over time.
- **Donation Analysis**: Visualizes donation trends, charity categories, and total donations for each charity.
- **User Demographics**: Analyzes user data by age group, region, and credit usage, and provides a heatmap of transaction volume.
- **Service Charges Overview**: Displays total service charges, average charge per user, and service charges by type and category.
- **Interactive Charts**: Uses different chart types (bar, pie, line, scatter, etc.) for easy data visualization.

## Tech Stack

- **Backend**: Python 3.x, Django, SQLite
- **Frontend**: HTML, CSS, JavaScript (for charting with libraries like Chart.js)
- **ETL**: Python (for the ETL process)
- **Database**: SQLite

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/data-warehouse-dashboard.git
    cd data-warehouse-dashboard
    ```

2. **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run database migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Start the development server:**

    ```bash
    python manage.py runserver
    ```

6. **Access the dashboard**: Open your browser and go to `http://127.0.0.1:8000/`.

## How It Works

### ETL Process
The ETL process is triggered from the dashboard by calling the `/trigger_etl/` route. The script loads data into the SQLite database, processes it, and prepares it for visualization.

### Data Visualizations
Data is retrieved from the SQLite database using SQL queries and visualized using JavaScript libraries such as Chart.js. Different routes handle the aggregation of data and render the appropriate charts for each section:

- **Unified Charts**: Displays transaction types, monthly transactions, and active vs. inactive users.
- **Donation Analysis**: Displays total donations, charity categories, and the total donation amount per charity.
- **User Demographics**: Provides insights into users' age groups, regions, and credit usage.
- **Service Charges Overview**: Analyzes service charges across different types and categories.

### Database Structure
The project uses several key models:

- `TransactionFact`: Contains transaction details.
- `DateDimension`: Represents time-related information (e.g., month, year).
- `CharityDimension`: Stores charity-related data.
- `ServiceDimension`: Contains service-related data.
- `UserDemographicsDimension`: Holds demographic information of users.
- `TransactionTypeDimension`: Represents the different types of transactions.

## Data Sources

- **Transaction Data**: Contains transaction amounts and details such as transaction type, date, and involved services.
- **Charity Data**: Tracks donations made to charities.
- **User Data**: Includes user demographics like age group and region.
- **Service Data**: Contains information about different services provided.

## Screenshots

*Add relevant screenshots here to showcase the app's interface and charts.*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Chart.js for data visualization.
- SQLite for simple and fast database management.
- Django for the backend framework.
- Python for the ETL process and backend scripting.


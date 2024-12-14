from django.shortcuts import render
from django.http import HttpResponse
import os
import subprocess
from .models import TransactionFact, DateDimension,CharityDimension
from django.db.models import Sum,Count
from .models import ServiceDimension, ServiceCategoryDimension
import sqlite3
from .models import UserDemographicsDimension, TransactionFact, TransactionTypeDimension
import json
from datetime import datetime



def trigger_etl(request):
    etl_script_path = os.path.join(os.path.dirname(__file__), 'etl.py')
    try:
        subprocess.run(['python', etl_script_path], check=True)
        return HttpResponse("ETL process completed successfully!")
    except Exception as e:
        return HttpResponse(f"ETL process failed: {str(e)}")


def unified_charts(request):
    # Connect to SQLite database
    db_path = "datawarehouse.db"  # Replace with your database path
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Chart 1: Total Transactions by Transaction Type
    query1 = """
        SELECT t.transaction_type, COUNT(f.transaction_id) AS total_transactions
        FROM Transaction_Fact f
        JOIN Transaction_Type_Dimension t ON f.transaction_type_id = t.transaction_type_id
        GROUP BY t.transaction_type
    """
    cursor.execute(query1)
    data1 = cursor.fetchall()
    transaction_types = [row[0] for row in data1]
    transaction_counts = [row[1] for row in data1]

    # Chart 2: Monthly Transactions
    query2 = """
        SELECT d.month, SUM(f.amount) AS total_amount
        FROM Transaction_Fact f
        JOIN Date_Dimension d ON f.date_id = d.date_id
        GROUP BY d.month
        ORDER BY d.month
    """
    cursor.execute(query2)
    data2 = cursor.fetchall()
    months = [row[0] for row in data2]
    monthly_totals = [row[1] for row in data2]

    # Chart 3: Counts the total transactions for active and inactive users
    query3 = """
        SELECT u.is_active, COUNT(f.transaction_id) AS total_transactions
        FROM Transaction_Fact f
        JOIN User_Dimension u ON f.user_id = u.user_id
        GROUP BY u.is_active
    """
    cursor.execute(query3)
    data3 = cursor.fetchall()
    user_types = ['Active' if row[0] else 'Inactive' for row in data3]
    user_transaction_counts = [row[1] for row in data3]

    # Chart 4: Transaction Volume Over Time
    query4 = """
        SELECT d.year || '-' || d.month || '-' || d.day AS date, SUM(f.amount) AS total_volume
        FROM Transaction_Fact f
        JOIN Date_Dimension d ON f.date_id = d.date_id
        GROUP BY d.year, d.month, d.day
        ORDER BY d.year, d.month, d.day
    """
    cursor.execute(query4)
    data4 = cursor.fetchall()
    dates = [row[0] for row in data4]
    cumulative_volumes = [row[1] for row in data4]

    # Calculate summary data for cards
    total_transactions = sum(transaction_counts)
    total_amount = sum(monthly_totals)
    total_active_users = sum([row[1] for row in data3 if row[0] == 1])
    total_inactive_users = sum([row[1] for row in data3 if row[0] == 0])

    # Close the database connection
    conn.close()

    # Pass data to the template
    context = {
        "transaction_types": json.dumps(transaction_types),
        "transaction_counts": json.dumps(transaction_counts),
        "months": json.dumps(months),
        "monthly_totals": json.dumps(monthly_totals),
        "user_types": json.dumps(user_types),
        "user_transaction_counts": json.dumps(user_transaction_counts),
        "dates": json.dumps(dates),
        "cumulative_volumes": json.dumps(cumulative_volumes),
        
        # Cards summary data
        "total_transactions": total_transactions,
        "total_amount": total_amount,
        "total_active_users": total_active_users,
        "total_inactive_users": total_inactive_users,
    }
    return render(request, "charts/unified_charts.html", context)



def donation_analysis(request):
    import sqlite3
    import json

    
    db_path = "datawarehouse.db"  
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Total Donations by Charity Category (Bar Chart & Pie Chart)
    query1 = """
        SELECT cc.category_name, SUM(f.amount) AS total_donations
        FROM Transaction_Fact f
        JOIN Charity_Dimension c ON f.charity_id = c.charity_id
        JOIN Charity_Category_Dimension cc ON c.charity_category_id = cc.charity_category_id
        GROUP BY c.charity_category_id
    """
    cursor.execute(query1)
    data1 = cursor.fetchall()
    categories = [row[0] for row in data1]
    donation_amounts = [row[1] for row in data1]

    # Calculate total donations and percentages
    total_donations = sum(donation_amounts)
    donation_percentages = [(amount / total_donations) * 100 if total_donations > 0 else 0 for amount in donation_amounts]

    # 3. Total Charity Donations Over Time (Line Chart)
    query3 = """
        SELECT d.year, d.month, SUM(f.amount) AS total_donations
        FROM Transaction_Fact f
        JOIN Date_Dimension d ON f.date_id = d.date_id
        GROUP BY d.year, d.month
        ORDER BY d.year, d.month
    """
    cursor.execute(query3)
    data3 = cursor.fetchall()
    dates = [f"{row[0]}-{row[1]}" for row in data3]
    donation_totals = [row[2] for row in data3]

    # 5. Total Donations for Each Charity (Bar Chart)
    query5 = """
      SELECT 
    c.name AS charity_name,
    COALESCE(SUM(tf.amount), 0) AS total_donations
FROM 
    Charity_Dimension c
LEFT JOIN 
    Transaction_Fact tf ON c.charity_id = tf.charity_id 
    AND tf.transaction_type_id = (SELECT transaction_type_id FROM Transaction_Type_Dimension WHERE transaction_type = 'Donation')
GROUP BY 
    c.name
ORDER BY 
    total_donations DESC;
    """
    cursor.execute(query5)
    data5 = cursor.fetchall()
    charities = [row[0] for row in data5]
    charity_totals = [row[1] for row in data5]

    # 6. Count of Distinct Charities
    query_distinct_charities = """
        SELECT COUNT(DISTINCT name)
        FROM Charity_Dimension;
    """
    cursor.execute(query_distinct_charities)
    distinct_charity_count = cursor.fetchone()[0]

    # 7. Count of Charity Categories (Total categories)
    query_category_count = """
        SELECT COUNT(category_name)
        FROM Charity_Category_Dimension;
    """
    cursor.execute(query_category_count)
    category_count = cursor.fetchone()[0]

    # Close the database connection
    conn.close()

    # Pass data to the template
    context = {
        "categories": json.dumps(categories),
        "donation_amounts": json.dumps(donation_amounts),  # Still used for bar chart
        "donation_percentages": json.dumps(donation_percentages),  # For pie chart
        "dates": json.dumps(dates),
        "donation_totals": json.dumps(donation_totals),
        "charities": json.dumps(charities),
        "charity_totals": json.dumps(charity_totals),

        # Data for cards
        "total_donations": total_donations,
        "donations_over_time": sum(donation_totals),  # Example: total over time
        "charity_count": distinct_charity_count,  # Number of distinct charities
        "category_count": category_count,  # Total categories
    }

    return render(request, "charts/donation_analysis.html", context)



def user_demographics(request):
    # Connect to SQLite database
    db_path = "datawarehouse.db"  # Replace with your database path
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Chart 1: Active Users by Age Group
    query1 = """
        SELECT d.age_group, COUNT(u.user_id) AS active_users
        FROM User_Dimension u
        JOIN User_Demographics_Dimension d ON u.user_demographics_id = d.user_demographics_id
        WHERE u.is_active = 1
        GROUP BY d.age_group
    """
    cursor.execute(query1)
    data1 = cursor.fetchall()
    age_groups = [row[0] for row in data1]
    active_users = [row[1] for row in data1]

    # Chart 2: User Distribution by Region (Pie Chart)
    query2 = """
        SELECT d.region, COUNT(u.user_id) AS total_users
        FROM User_Dimension u
        JOIN User_Demographics_Dimension d ON u.user_demographics_id = d.user_demographics_id
        GROUP BY d.region
    """
    cursor.execute(query2)
    data2 = cursor.fetchall()
    regions = [row[0] for row in data2]
    user_counts = [row[1] for row in data2]

    # Chart 3: Heatmap - Transaction Volume by User Demographics and Time
    query3 = """
        SELECT d.region, dt.month, SUM(f.amount) AS transaction_volume
        FROM Transaction_Fact f
        JOIN User_Dimension u ON f.user_id = u.user_id
        JOIN User_Demographics_Dimension d ON u.user_demographics_id = d.user_demographics_id
        JOIN Date_Dimension dt ON f.date_id = dt.date_id
        GROUP BY d.region, dt.month
        ORDER BY d.region, dt.month
    """
    cursor.execute(query3)
    data3 = cursor.fetchall()
    heatmap_data = {}
    for row in data3:
        region, month, volume = row
        if region not in heatmap_data:
            heatmap_data[region] = {}
        heatmap_data[region][month] = volume

    # Chart 4: Scatter Plot - User Credit vs Transaction Amount
    query4 = """
        SELECT u.phone_credit, SUM(f.amount) AS transaction_amount
        FROM User_Dimension u
        JOIN Transaction_Fact f ON u.user_id = f.user_id
        GROUP BY u.phone_credit
    """
    cursor.execute(query4)
    data4 = cursor.fetchall()
    user_credits = [row[0] for row in data4]
    transaction_amounts = [row[1] for row in data4]

    # KPI Cards:
    # Total Users
    query5 = "SELECT COUNT(*) FROM User_Dimension"
    cursor.execute(query5)
    total_users = cursor.fetchone()[0]

    # Active Users
    query6 = "SELECT COUNT(*) FROM User_Dimension WHERE is_active = 1"
    cursor.execute(query6)
    active_users_count = cursor.fetchone()[0]

    # New Users This Month
    current_month = datetime.now().month
    query7 = """
        SELECT COUNT(*)
        FROM User_Dimension u
        JOIN Date_Dimension d ON u.user_id = d.date_id
        WHERE d.month = ?
    """
    cursor.execute(query7, (current_month,))
    new_users_this_month = cursor.fetchone()[0]

    # User Retention Rate
    query8 = """
        SELECT COUNT(*) * 1.0 / (
            SELECT COUNT(*) FROM User_Dimension
        ) AS retention_rate
        FROM User_Dimension
        WHERE is_active = 1
    """
    cursor.execute(query8)
    retention_rate = cursor.fetchone()[0]

    # Close the database connection
    conn.close()

    # Prepare data for the template
    context = {
        # Chart data
        "age_groups": json.dumps(age_groups),
        "active_users": json.dumps(active_users),
        "regions": json.dumps(regions),
        "user_counts": json.dumps(user_counts),
        "heatmap_data": json.dumps(heatmap_data),
        "user_credits": json.dumps(user_credits),
        "transaction_amounts": json.dumps(transaction_amounts),
        
        # KPI Cards
        "total_users": total_users,
        "active_users_count": active_users_count,
        "new_users_this_month": new_users_this_month,
        "retention_rate": round(retention_rate * 100, 2),  # Percentage format
    }
    return render(request, "charts/user_demographics.html", context)


def service_charges_overview(request):
    # Connect to SQLite database
    db_path = "datawarehouse.db"  # Replace with your database path
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query 1: Total Service Charges by Service Type (Bar Chart)
    query1 = """
        SELECT s.service_type, SUM(f.amount) AS total_charges
        FROM Transaction_Fact f
        JOIN Service_Dimension s ON f.service_id = s.service_id
        GROUP BY s.service_type
    """
    cursor.execute(query1)
    data1 = cursor.fetchall()
    service_types = [row[0] for row in data1]
    service_charges_by_type = [row[1] for row in data1]

    # Query 2: Service Charges by Category (Pie Chart)
    query2 = """
        SELECT c.category_name, SUM(f.amount) AS total_charges
        FROM Transaction_Fact f
        JOIN Service_Dimension s ON f.service_id = s.service_id
        JOIN Service_Category_Dimension c ON s.service_category_id = c.service_category_id
        GROUP BY c.category_name
    """
    cursor.execute(query2)
    data2 = cursor.fetchall()
    category_names = [row[0] for row in data2]
    service_charges_by_category = [row[1] for row in data2]

    # Query 3: Service Charges by Type and Category (Stacked Bar Chart)
    query3 = """
        SELECT t.transaction_type, c.category_name, SUM(f.amount) AS total_charges
        FROM Transaction_Fact f
        JOIN Transaction_Type_Dimension t ON f.transaction_type_id = t.transaction_type_id
        JOIN Service_Dimension s ON f.service_id = s.service_id
        JOIN Service_Category_Dimension c ON s.service_category_id = c.service_category_id
        GROUP BY t.transaction_type, c.category_name
    """
    cursor.execute(query3)
    data3 = cursor.fetchall()
    transaction_types = list(set([row[0] for row in data3]))  # Unique transaction types
    categories = list(set([row[1] for row in data3]))  # Unique categories
    service_charges_by_type_and_category = {tx: {cat: 0 for cat in categories} for tx in transaction_types}
    for row in data3:
        service_charges_by_type_and_category[row[0]][row[1]] = row[2]

    # Query 4: Service Charges by Service Type (Donut Chart)
    query4 = """
        SELECT s.service_type, SUM(f.amount) AS total_charges
        FROM Transaction_Fact f
        JOIN Service_Dimension s ON f.service_id = s.service_id
        GROUP BY s.service_type
    """
    cursor.execute(query4)
    data4 = cursor.fetchall()
    service_types_donut = [row[0] for row in data4]
    service_charges_by_type_donut = [row[1] for row in data4]

    # KPI 1: Total Service Charges
    query5 = """
        SELECT SUM(f.amount) AS total_charges
        FROM Transaction_Fact f
    """
    cursor.execute(query5)
    total_service_charges = cursor.fetchone()[0]

    # KPI 2: Average Service Charge per User
    query6 = """
        SELECT AVG(f.amount) AS avg_charge_per_user
        FROM Transaction_Fact f
    """
    cursor.execute(query6)
    avg_charge_per_user = cursor.fetchone()[0]

    # KPI 3: Service Charges This Month
    query7 = """
        SELECT SUM(f.amount) AS charges_this_month
        FROM Transaction_Fact f
        JOIN Date_Dimension d ON f.date_id = d.date_id
        WHERE d.month = strftime('%m', 'now') AND d.year = strftime('%Y', 'now')
    """
    cursor.execute(query7)
    charges_this_month = cursor.fetchone()[0]

    # KPI 4: Service Categories with the Highest Charges
    query8 = """
        SELECT c.category_name, SUM(f.amount) AS total_charges
        FROM Transaction_Fact f
        JOIN Service_Dimension s ON f.service_id = s.service_id
        JOIN Service_Category_Dimension c ON s.service_category_id = c.service_category_id
        GROUP BY c.category_name
        ORDER BY total_charges DESC
        LIMIT 5
    """
    cursor.execute(query8)
    top_categories = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Pass data to the template
    context = {
        # Chart Data
        "service_types": json.dumps(service_types),
        "service_charges_by_type": json.dumps(service_charges_by_type),
        "category_names": json.dumps(category_names),
        "service_charges_by_category": json.dumps(service_charges_by_category),
        "transaction_types": json.dumps(transaction_types),
        "categories": json.dumps(categories),
        "service_charges_by_type_and_category": json.dumps(service_charges_by_type_and_category),
        "service_types_donut": json.dumps(service_types_donut),
        "service_charges_by_type_donut": json.dumps(service_charges_by_type_donut),

        # KPI Data
        "total_service_charges": total_service_charges,
        "avg_charge_per_user": avg_charge_per_user,
        "charges_this_month": charges_this_month,
        "top_categories": top_categories,  # Passing as a list of tuples (category_name, total_charges)
    }

    return render(request, "charts/service_charges_overview.html", context)



def index(request):
    # Aggregate transaction amounts by month
    monthly_data = (
        TransactionFact.objects
        .values("date__month")
        .annotate(total_amount=Sum("amount"))
        .order_by("date__month")
    )
    
    months = [item["date__month"] for item in monthly_data]
    amounts = [float(item["total_amount"]) for item in monthly_data]  # Convert Decimal to float

    return render(request, "charts/index.html", {
        "months": months,
        "amounts": amounts
    })





def charity_chart(request):
    # Connect to the SQLite database
    db_path = "datawarehouse.db"  # Replace with your actual database path
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to get the total donations by charity category
    query = """
        SELECT c.category_name, SUM(d.amount) AS total_donations
        FROM Charity_Dimension d
        JOIN Charity_Category_Dimension c ON d.charity_category_id = c.charity_category_id
        GROUP BY c.category_name
    """
    cursor.execute(query)
    
    # Fetch data
    data = cursor.fetchall()

    # Process data into categories and donation amounts
    categories = [item[0] for item in data]
    donations = [float(item[1]) for item in data]  # Convert Decimal to float

    # Close the connection
    conn.close()

    # Pass data to the template
    return render(request, "charts/charity_chart.html", {
        "categories": categories,
        "donations": donations,
    })


def service_charge_chart(request):
    # Connect to the SQLite database (replace 'r.db' with the actual path to your database)
    db_path = "datawarehouse.db"  # Path to your SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to get total charges by service type
    query = """
        SELECT s.service_type, SUM(t.amount) AS total_charges
        FROM Service_Dimension s
        JOIN Transaction_Fact t ON s.service_id = t.service_id
        GROUP BY s.service_type
    """
    cursor.execute(query)

    # Fetch data
    data = cursor.fetchall()

    # Process data into service types and charges
    service_types = [item[0] for item in data]
    charges = [float(item[1]) for item in data]  # Convert Decimal to float

    # Close the connection
    conn.close()

    # Pass data to the template
    return render(request, "charts/service_charge_chart.html", {
        "service_types": service_types,
        "charges": charges,
    })




def distribution_charts(request):
    # Query to get the User Distribution by Region
    user_data = UserDemographicsDimension.objects.values("region").annotate(user_count=Count("userdimension"))
    regions = [item["region"] for item in user_data]
    user_counts = [item["user_count"] for item in user_data]

    # Query to get the Transaction Distribution by Type
    transaction_data = TransactionFact.objects.values("transaction_type__transaction_type").annotate(transaction_count=Count("transaction_id"))
    transaction_types = [item["transaction_type__transaction_type"] for item in transaction_data]
    transaction_counts = [item["transaction_count"] for item in transaction_data]

    # Pass data to the template
    return render(request, "charts/distribution_charts.html", {
        "regions": regions,
        "user_counts": user_counts,
        "transaction_types": transaction_types,
        "transaction_counts": transaction_counts,
    })


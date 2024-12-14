import logging
from django.core.management.base import BaseCommand
from django.db import connections, transaction, IntegrityError
from etl_app.models import (
    UserDemographicsDimension,
    UserDimension,
    ServiceCategoryDimension,
    ServiceDimension,
    CharityCategoryDimension,
    CharityDimension,
    DateDimension,
    TransactionTypeDimension,
    TransactionFact,
)
from datetime import datetime

logging.basicConfig(
    filename="data_import.log",
    level=logging.DEBUG,  # Set to DEBUG for more detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class Command(BaseCommand):
    help = "Imports data from the SQLite source database into Django models"

    def handle(self, *args, **kwargs):
        source_conn = connections["source_db"] 

        # Define mappings between models and database tables
        data_mappings = [
            {"model": UserDemographicsDimension, "table": "User_Demographics_Dimension"},
            {"model": UserDimension, "table": "User_Dimension"},
            {"model": ServiceCategoryDimension, "table": "Service_Category_Dimension"},
            {"model": ServiceDimension, "table": "Service_Dimension"},
            {"model": CharityCategoryDimension, "table": "Charity_Category_Dimension"},
            {"model": CharityDimension, "table": "Charity_Dimension"},
            {"model": DateDimension, "table": "Date_Dimension"},
            {"model": TransactionTypeDimension, "table": "Transaction_Type_Dimension"},
            {"model": TransactionFact, "table": "Transaction_Fact"},
        ]

        for mapping in data_mappings:
            self.import_data(source_conn, mapping["model"], mapping["table"])

    def import_data(self, source_conn, model, table_name):
        """Imports data from the source database table into the Django model."""
        self.stdout.write(f"Importing data for model {model.__name__} from {table_name}...")
        logging.info(f"Importing data for model {model.__name__} from {table_name}...")

        try:
            with source_conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table_name}")
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()

                # Create model instances
                objects = []
                for row in rows:
                    # Prepare the row data
                    data = dict(zip(columns, row))
                    
                    # Log raw data for inspection
                    logging.debug(f"Raw data for {model.__name__}: {data}")

                   
                    # Check for foreign key relationships, e.g., UserDemographicsDimension for UserDimension
                    if model == UserDimension and 'user_demographics_id' in data:
                        user_demographics_id = data['user_demographics_id']
                        if not UserDemographicsDimension.objects.filter(user_demographics_id=user_demographics_id).exists():
                            logging.warning(f"UserDemographicsDimension with ID {user_demographics_id} not found. Skipping UserDimension record.")
                            continue

                    # Create model instance
                    try:
                        objects.append(model(**data))
                    except IntegrityError as e:
                        logging.error(f"Integrity error while inserting data into {model.__name__}: {e}")
                        continue






















































































































































































































































































































                # Bulk create objects in the database
                if objects:
                    with transaction.atomic():
                        model.objects.bulk_create(objects, batch_size=1000)

                    self.stdout.write(f"Successfully imported {len(objects)} records into {model.__name__}.")
                    logging.info(f"Successfully imported {len(objects)} records into {model.__name__}.")
                else:
                    self.stdout.write(f"No valid data to import for {model.__name__}.")
                    logging.warning(f"No valid data to import for {model.__name__}.")

        except Exception as e:
            self.stderr.write(f"Error importing data for {model.__name__}: {e}")
            logging.error(f"Error importing data for {model.__name__}: {e}")

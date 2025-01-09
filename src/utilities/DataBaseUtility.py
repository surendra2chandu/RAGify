# Importing the required libraries
from src.conf.Configurations import logger
import psycopg2


class DataBaseUtility:
    def __init__(self, db_config):

        # Set the database configuration
        self.db_config = db_config

        # Connect to the database
        logger.info("Connecting to the database...")
        self.conn = psycopg2.connect(**self.db_config)

        # Create a cursor object
        cursor = conn.cursor()


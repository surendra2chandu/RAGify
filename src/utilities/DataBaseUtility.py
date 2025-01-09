# Importing the required libraries
from src.conf.Configurations import logger, db_config
import psycopg2


class DataBaseUtility:
    def __init__(self):
        """
        This function initializes the DataBaseUtility class with the specified database configuration.
        """

        # Set the database configuration
        self.db_config = db_config

        # Connect to the database
        logger.info("Connecting to the database...")
        self.conn = psycopg2.connect(**self.db_config)

        # Create a cursor object
        self.cursor = self.conn.cursor()


    # Function to store chunks in the database
    def store_chunks_in_db(self, chunks):
        """
        This function stores the chunks in the database.
        :param chunks: The chunks to be stored.
        :return: None
        """

        # Drop the table if it exists
        logger.info("Dropping the table if it exists...")
        self.cursor.execute("DROP TABLE IF EXISTS document_chunks;")

        # Create the table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS document_chunks (
                id SERIAL PRIMARY KEY,
                chunk TEXT,
                embedding FLOAT8[]  -- Array of floats for embeddings
            );
        """)

        # Insert the data
        logger.info("Inserting data into the database...")
        for chunk_text, chunk_embedding in chunks:
            chunk_embedding_list = chunk_embedding.astype(float).tolist()  # Convert numpy array to list of floats

            self.cursor.execute(
                """
                INSERT INTO document_chunks (chunk, embedding)
                VALUES (%s, %s)
                """,
                (chunk_text, chunk_embedding_list),
            )

        # Commit the changes
        logger.info("Committing the changes...")
        self.conn.commit()

        # Close the cursor and connection
        logger.info("Closing the cursor and connection...")
        self.cursor.close()
        self.conn.close()


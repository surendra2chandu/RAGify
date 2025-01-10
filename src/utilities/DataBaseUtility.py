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

        # Create the table if it doesn't exist (Using pgvector's vector type for embeddings)
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS document_chunks (
                        id SERIAL PRIMARY KEY,
                        chunk TEXT,
                        embedding vector  
                    );
                """)

        # Insert the data
        for chunk_text, chunk_embedding in chunks:
            chunk_embedding_list = chunk_embedding.astype(float).tolist()  # Convert numpy array to list of floats

            self.cursor.execute(
                """
                INSERT INTO document_chunks (chunk, embedding)
                VALUES (%s, %s::vector)  -- Cast the embedding to the vector type
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


    def fetch_similar_text(self, query_embedding):
        """
        This function retrieves all matches for the query sorted by similarity in descending order.
        :param query_embedding: The embedding of the query.
        :return: The results sorted by similarity in descending order.
        """


        # Retrieve all matches sorted by similarity in descending order
        logger.info("Retrieving all matches for the query...")
        self.cursor.execute(
            """
            SELECT chunk, 1 - (embedding <=> %s::vector) AS similarity
            FROM document_chunks
            ORDER BY similarity DESC;
            """,
            (query_embedding.tolist(),)
        )

        # Fetch the results
        logger.info("Fetching the results...")
        results = self.cursor.fetchall()

        # Close the cursor and connection
        logger.info("Closing the cursor and connection...")
        self.cursor.close()
        self.conn.close()

        # Return the results
        return results


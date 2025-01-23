# Importing the required libraries
from src.web_scraping.DataExtractor import DataExtractor
from src.utilities.LateChunking import LateChunking
from src.conf.Configurations import logger
from src.utilities.DataBaseUtility import DataBaseUtility
from src.utilities.GetTokenEmbeddings import GetTokenEmbeddings
import os


class WebDataInjector:

    # Main function to process PDF and store chunks
    def process_data_and_store(self, url):
        """
        This function extracts data from the specified URL and stores the chunks in the database.
        :param url:
        :return: None
        """

        # Extract data from the URL
        data = DataExtractor().extract_data(url)

        for doc_name, text in data.items():
            # Tokenize and get embeddings
            logger.info("Tokenizing and embedding text...")
            tokens, embeddings = GetTokenEmbeddings().tokenize_and_embed(text[:500])

            # Perform late chunking
            logger.info("Performing late chunking...")
            chunks = LateChunking().late_chunk(tokens, embeddings)

            # Store chunks in database
            logger.info("Storing chunks in the database...")
            DataBaseUtility().store_chunks_in_db(chunks, doc_name)

# Run the script
if __name__ == "__main__":


    sample_db_config = {
        "dbname": "langchain",
        "user": "langchain",
        "password": "langchain",
        "host": "localhost",
        "port": 5432,
    }

    # URL of the website
    sample_url = "https://www.defense.gov/news/"

    # Process the data and store the chunks
    WebDataInjector().process_data_and_store(sample_url)

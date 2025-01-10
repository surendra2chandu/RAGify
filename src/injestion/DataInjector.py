# Importing the required libraries
from src.utilities.PDFDataExtractor import PDFDataExtractor
from src.utilities.LateChunking import LateChunking
from src.conf.Configurations import logger
from src.utilities.DataBaseUtility import DataBaseUtility
from src.utilities.GetTokenEmbeddings import GetTokenEmbeddings


class DataInjector:

    # Main function to process PDF and store chunks
    def process_pdf_and_store(self, pdf_path):
        """
        This function processes a PDF file and stores the chunks in the database.
        :param pdf_path: The path to the PDF file.
        :return: None
        """

        # Extract text from PDF
        logger.info("Extracting text from PDF...")
        text = PDFDataExtractor().extract_text_from_pdf(pdf_path)

        # Tokenize and get embeddings
        logger.info("Tokenizing and embedding text...")
        tokens, embeddings = GetTokenEmbeddings().tokenize_and_embed(text)

        # Perform late chunking
        logger.info("Performing late chunking...")
        chunks = LateChunking().late_chunk(tokens, embeddings)

        # Store chunks in database
        logger.info("Storing chunks in the database...")
        DataBaseUtility().store_chunks_in_db(chunks)


# Run the script
if __name__ == "__main__":

    # Sample PDF path
    sample_pdf_path = r'C:\Docs\doc5.pdf'

    sample_db_config = {
        "dbname": "langchain",
        "user": "langchain",
        "password": "langchain",
        "host": "localhost",
        "port": 5432,
    }

    DataInjector().process_pdf_and_store(sample_pdf_path)

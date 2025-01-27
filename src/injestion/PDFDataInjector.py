# Importing the required libraries
from src.utilities.PDFDataExtractor import PDFDataExtractor
from src.utilities.LateChunking import LateChunking
from src.conf.Configurations import logger, DOC_TYPE_FOR_PDF
from src.utilities.DataBaseUtility import DataBaseUtility
from src.utilities.GetTokenEmbeddings import GetTokenEmbeddings
import os


class PDFDataInjector:

    # Main function to process PDF and store chunks
    def process_pdf_and_store(self, pdf_path, file_name):
        """
        This function extracts text from the specified PDF and stores the chunks in the database.
        :param pdf_path: The path to the PDF file.
        :param file_name: The name of the file.
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
        DataBaseUtility().store_chunks_in_db(chunks, file_name, DOC_TYPE_FOR_PDF)

# Run the script
if __name__ == "__main__":

    # Sample PDF path
    sample_pdf_path = r'C:\Docs\sample_doc.pdf'

    sample_file_name = os.path.splitext(os.path.basename(sample_pdf_path))[0]

    sample_db_config = {
        "dbname": "langchain",
        "user": "langchain",
        "password": "langchain",
        "host": "localhost",
        "port": 5432,
    }

    PDFDataInjector().process_pdf_and_store(sample_pdf_path, sample_file_name)

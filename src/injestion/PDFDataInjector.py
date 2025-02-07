# Importing the required libraries
from src.utilities.PDFDataExtractor import PDFDataExtractor
from src.utilities.InjectionUtility import InjectionUtility
from src.conf.Configurations import logger
from src.utilities.DataBaseUtility import DataBaseUtility
import os


class PDFDataInjector:

    @staticmethod
    def process_pdf_and_store( pdf_path, file_name):
        """
        This function extracts text from the specified PDF and stores the chunks in the database.
        :param pdf_path: The path to the PDF file.
        :param file_name: The name of the file.
        :return: None
        """

        if DataBaseUtility().document_exists(file_name):
            logger.info(f"Document '{file_name}' already exists in the database. Skipping...")
            return

        # Extract text from PDF
        logger.info("Extracting text from PDF...")
        text = PDFDataExtractor().extract_text_from_pdf(pdf_path)

        # Process the text pipeline
        logger.info("Processing text pipeline...")
        InjectionUtility().process_text_pipeline(text, file_name)

        # Commit and close the database connection
        logger.info("Committing and closing the database connection...")
        DataBaseUtility().commit_and_close()

# Run the script
if __name__ == "__main__":

    # Sample PDF path
    sample_pdf_path = r'C:\Docs\sample_doc.pdf'

    # Extract the file name from the PDF path
    sample_file_name = os.path.splitext(os.path.basename(sample_pdf_path))[0]

    # Process the PDF and store the chunks in the database
    PDFDataInjector().process_pdf_and_store(sample_pdf_path, sample_file_name)

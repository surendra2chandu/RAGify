# Importing the required libraries
from src.utilities.PDFDataExtractor import PDFDataExtractor
from src.utilities.InjectionUtility import InjectionUtility
from src.conf.Configurations import logger
from src.utilities.DataBaseUtility import DataBaseUtility
import os
from fastapi import HTTPException


class PDFDataInjector:

    @staticmethod
    def get_pdf_files(directory_path: str):
        """
        Returns a list of all PDF files in the given directory.

        :param directory_path: Path to the directory containing PDF files.
        :return: List of PDF file paths.
        """
        if not os.path.isdir(directory_path):
            raise HTTPException(status_code=400, detail=f"Invalid directory: {directory_path}")

        pdf_files = [
            os.path.join(directory_path, file)
            for file in os.listdir(directory_path)
            if file.lower().endswith('.pdf')
        ]

        if not pdf_files:
            # to-do
            raise HTTPException(status_code=404, detail="No PDF files found in the directory.")

        return pdf_files

    @staticmethod
    def process_pdf_and_store( file,):
        """
        Extracts text from the PDF and stores the processed chunks in the database.
        :param file: Path to the PDF file.
        :return: None
        """

        # Extract text from PDF
        logger.info(f"Extracting text from PDF: {file}")
        text = PDFDataExtractor().extract_text_from_pdf(file)

        if not text:
            logger.warning(f"No text extracted from {file}. Skipping...")
            return
        file_name = os.path.splitext(os.path.basename(file))[0]
        # Process the text pipeline
        logger.info("Processing text pipeline...")
        InjectionUtility().process_text_pipeline(text, file_name)

    def process_files(self, directory_path):
        """
        Processes all PDF files in the given directory.
        :param directory_path: Path to the directory containing PDF files.
        :return: None
        """

        # Get a list of all PDF files in the directory
        logger.info(f"Processing PDF files in directory: {directory_path}")
        pdf_files = self.get_pdf_files(directory_path)

        for file in pdf_files:
            try:
                # Process each PDF file
                logger.info(f"Processing PDF file: {file}")
                self.process_pdf_and_store(file)
            except Exception as e:
                # Log the error and raise an exception
                logger.error(f"An error occurred while processing {file}: {e}")
                raise HTTPException(status_code=500, detail=f"An error occurred while processing {file}: {e}")

        # Commit and close the database connection
        logger.info("Committing and closing the database connection...")
        DataBaseUtility().commit_and_close()

# Run the script
if __name__ == "__main__":
    pdf_directory = r'C:\Docs'  # Update with your directory path
    PDFDataInjector().process_files(pdf_directory)

# Importing the required libraries
from src.utilities.PDFDataExtractor import PDFDataExtractor
from src.utilities.LateChunking import LateChunking
from src.conf.Configurations import logger, DOC_TYPE_FOR_PDF
from src.utilities.DataBaseUtility import DataBaseUtility
from src.utilities.GetTokenEmbeddings import GetTokenEmbeddings
import os


class PDFDataInjector:

    def process_pdf_and_store(self, pdf_path, file_name):
        """
        Extracts text from the PDF and stores the processed chunks in the database.
        :param pdf_path: Path to the PDF file.
        :param file_name: Name of the file.
        :return: None
        """

        # Extract text from PDF
        logger.info(f"Extracting text from PDF: {file_name}")
        text = PDFDataExtractor().extract_text_from_pdf(pdf_path)

        if not text:
            logger.warning(f"No text extracted from {file_name}. Skipping...")
            return

        # Tokenize and get embeddings
        logger.info(f"Tokenizing and embedding text for: {file_name}")
        tokens, embeddings = GetTokenEmbeddings().tokenize_and_embed(text)

        # Perform late chunking
        logger.info(f"Performing late chunking for: {file_name}")
        chunks = LateChunking().late_chunk(tokens, embeddings)

        # Store chunks in database
        logger.info(f"Storing chunks in the database for: {file_name}")
        DataBaseUtility().store_chunks_in_db(chunks, file_name, DOC_TYPE_FOR_PDF)

    def process_directory(self, directory_path):
        """
        Processes all PDF files in the given directory.
        :param directory_path: Path to the directory containing PDF files.
        :return: None
        """
        if not os.path.isdir(directory_path):
            logger.error(f"Invalid directory: {directory_path}")
            return

        for file in os.listdir(directory_path):
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(directory_path, file)
                file_name = os.path.splitext(file)[0]

                if DataBaseUtility().document_exists(file_name):
                    logger.info(f"Document '{file_name}' already exists in the database. Skipping...")
                    continue

                self.process_pdf_and_store(pdf_path, file_name)


# Run the script
if __name__ == "__main__":
    pdf_directory = r'C:\Docs'  # Update with your directory path
    PDFDataInjector().process_directory(pdf_directory)

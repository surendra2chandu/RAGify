# Import the necessary packages
from PyPDF2 import PdfReader
from src.conf.Configurations import logger


class PDFDataExtractor:

    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from a PDF file.
        :param pdf_path: Path to the PDF file.
        :return: Extracted text from the PDF file.
        """

        # Read the PDF file
        reader = PdfReader(pdf_path)

        # Initialize the text
        text = ""

        # Iterate over the pages
        for page_number in range(len(reader.pages)):
            text += reader.pages[page_number].extract_text()

        # Return the extracted text
        return text


if __name__ == '__main__':
    pdf_data_extractor = PDFDataExtractor()
    sample_pdf_path = r'C:\Docs\doc5.pdf'
    extracted_text = pdf_data_extractor.extract_text_from_pdf(sample_pdf_path)
    print(extracted_text)
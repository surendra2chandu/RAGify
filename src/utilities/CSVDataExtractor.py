# Importing the required libraries
import pandas as pd
from src.conf.Configurations import logger

class CSVDataExtractor:

    @staticmethod
    def extract_data(csv_file_path: str) -> str:
        """
        Extracts data from a CSV file and returns complete text as a string.
        :param csv_file_path: The path to the CSV file.
        :return: The complete text extracted from the CSV file.
        """

        # Read CSV while ensuring all data is treated as text
        logger.info(f"Reading data from CSV file: {csv_file_path}")
        df = pd.read_csv(csv_file_path, dtype=str, skiprows=lambda x: x in [1, 2])

        # Concatenate heading and intro columns
        logger.info("Concatenating heading and intro columns...")
        output_text = " . ".join(f"{row['heading']}: {row['intro']}" for _, row in df.iterrows())

        # Return the complete text
        return output_text

if __name__ == "__main__":
    print(CSVDataExtractor.extract_data("sample_data.csv"))







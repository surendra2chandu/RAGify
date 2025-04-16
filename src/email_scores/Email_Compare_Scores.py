# Import necessary libraries
from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from src.conf.Configurations import model_path,logger
from fastapi import HTTPException
import pandas as pd
import numpy as np

class EmailSimilarity:
    """
    A class to compare email addresses based on the similarity of their names using embeddings.
    """

    def __init__(self, list1, list2):
        """
        Initialize the EmailSimilarity class.

        :param list1: First list of email addresses.
        :param list2: Second list of email addresses.
        """
        try:
            self.model_name = model_path
            self.model = HuggingFaceEmbeddings(model_name=self.model_name)
            logger.info(f"Loading model from {self.model_name}...")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred during model loading: {e}")

        self.list1 = list1
        self.list2 = list2
        self.results = []

    @staticmethod
    def get_name(email):
        """
        Extract the name from the email address.

        :param email: The email address.
        :return: The name part of the email address.
        """

        return email.split('@')[0].replace('.', ' ').replace('_', ' ').strip()

    def compare_emails(self):
        """
        Compare two lists of email addresses and calculate the similarity scores.
        """
        try:
            # Extract names from emails
            names1 = [self.get_name(email) for email in self.list1]
            names2 = [self.get_name(email) for email in self.list2]

            # Generate embeddings
            embeddings1 = self.model.embed_documents(names1)
            embeddings2 = self.model.embed_documents(names2)

            # Convert embeddings to numpy arrays
            emb1 = np.array(embeddings1)
            emb2 = np.array(embeddings2)

            # Calculate cosine similarity
            #sim_scores  = cosine_similarity(emb1, emb2).diagonal()
            sim_scores = np.round(cosine_similarity(emb1, emb2).diagonal(), 3)

            # Store results
            self.results = list(zip(self.list1, self.list2,sim_scores ))
            print()
        except Exception as e:
            logger.error(f"Error during email comparison: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during email comparison: {e}")

    def write_to_csv(self, filename='pairwise_email_scores.csv'):
        """
        Write the similarity scores to a CSV file.
        :param filename: The name of the output CSV file.
        """
        try:
            # Create a DataFrame
            dataframe = pd.DataFrame(self.results, columns=['Email1', 'Email2', 'Embedding Score'])
            dataframe.to_csv(filename, index=False)
            print(f"Scores written to '{filename}'")
        except Exception as e:
            logger.error(f"Error writing to CSV: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred while writing to CSV: {e}")

# Main function to execute the script
if __name__ == "__main__":

    # Read the CSV file containing the lists of emails
    file_path = r"D:\CSV\ListOfEmails.csv"
    df = pd.read_csv(file_path)

    listA = df['ListA'].tolist()
    listB = df['ListB'].tolist()

    # Create an instance of the EmailSimilarity class and compare emails
    similarity_checker = EmailSimilarity(listA, listB)
    similarity_checker.compare_emails()
    similarity_checker.write_to_csv()

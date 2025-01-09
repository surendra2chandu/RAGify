import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DocumentSimilarity:
    def __init__(self, corpus):
        """
        Initializes the DocumentSimilarity class.
        :param corpus: The list of documents in the corpus.
        """
        self.corpus = corpus
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

    def top2_documents(self, query):
        """
        This method performs cosine similarity checks between a given query and the documents in the corpus
        to log the top 2 most similar documents.
        :param query: The input query to compare with the documents.
        :return: None
        """

        # Transform the query using the same vectorizer
        query_vec = self.vectorizer.transform([query])

        # Compute the cosine similarity between the query and all documents
        cosine_similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Get the indices of the top 2 most similar documents
        top_2_query = np.argsort(cosine_similarities)[-2:][::-1]

        # Log the top 2 most similar documents and their cosine similarity score
        logging.info(f"Top 2 documents most similar to the query '{query}':")
        for index in top_2_query:
            logging.info(f"Sentence: '{self.corpus[index]}' | Cosine similarity score: {cosine_similarities[index]}")

if __name__ == "__main__":

    # Sample query
    sample = "adi narayana "

    documents = [
        "This is the first document",
        "This document is the second document",
        "And this is the third one ",
        "Is this the first document adi",
        "Is this the first first document first adi narayana choudary reddy"
    ]

    # Initialize the DocumentSimilarity class
    document_similarity = DocumentSimilarity(documents)

    #top2_documents function is called
    document_similarity.top2_documents(sample)



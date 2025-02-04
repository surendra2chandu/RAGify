# Importing necessary classes,libraries and modules
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from src.conf.Configurations import logger, NUMBER_OF_MATCHES
from src.utilities.DataBaseUtility import DataBaseUtility


# Set up logging configuration
class QueryVectorizer:

    def __init__(self):
        """
        Initializes the DocumentSimilarity class.
        """

        self.corpus = DataBaseUtility().extract_doc_content()
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)

    def extract_docs(self, query):
        """
        This function extracts the top most similar documents to the query.
        :param query: The query to search for.
        :return: The top most similar documents to the query.
        """

        # Transform the query using the same vectorizer
        query_vec = self.vectorizer.transform([query])

        # Compute the cosine similarity between the query and all documents
        cosine_similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Get the indices of the top 2 most similar documents
        top_3_query = np.argsort(cosine_similarities)[-NUMBER_OF_MATCHES:][::-1]

        result = []

        # Log the top 2 most similar documents and their cosine similarity score
        logger.info(f"Top 3 documents most similar to the query '{query}':")
        for index in top_3_query:
            logger.info(f"Sentence: '{self.corpus[index]}' | Confidence level: {cosine_similarities[index]}")
            result.append((self.corpus[index], cosine_similarities[index]))

        return result

if __name__ == "__main__":

    # Sample query
    sample= "lcsp process graphic aflcmc classified lcsp process 2020pptx attachment 16 change management plan attachment 16change management plandoc"

    #top2_documents function is called
    res = QueryVectorizer().extract_docs(sample)
    print(res)




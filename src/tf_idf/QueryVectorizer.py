
# Importing necessary classes,libraries and modules
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from src.conf.Configurations import logger


# Set up logging configuration
class QueryVectorizer:
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
        logger.info(f"Top 2 documents most similar to the query '{query}':")
        for index in top_2_query:
            logger.info(f"Sentence: '{self.corpus[index]}' | Cosine similarity score: {cosine_similarities[index]}")

        res = dict()

        res["top_2_query"] = top_2_query

        res["cosine_similarities"] = cosine_similarities

        return res

if __name__ == "__main__":

    # Sample query
    sample = "sun "

    documents = [
        "The sun sets behind the mountains, casting a golden glow.",
        "The sun warmed the beach as we walked along the shore.",
        "She picked up her book and opened to the first page.",
        "After a long day, he relaxed with a hot cup of tea.",
        "The warm air by the beach made the evening even more pleasant."
    ]

    # Initialize the DocumentSimilarity class
    document_similarity = QueryVectorizer(documents)

    #top2_documents function is called
    res = document_similarity.top2_documents(sample)

    print(res)



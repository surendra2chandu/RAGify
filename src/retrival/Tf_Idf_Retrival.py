# Import necessary libraries , classes and functions
import psycopg2
from sklearn.feature_extraction.text import TfidfVectorizer

from src.conf.Configurations import db_config, NUMBER_OF_MATCHES_FOR_TF_IDF, logger
from src.injestion.Tf_Idf_Injector import TfIdfInjector

class TfIdfRetrival:

    @staticmethod
    def retrieve_relevant_docs(query: str):
        """
        Extracts documents similar to the query using TF-IDF.

        :param query: The query to search for.
        :return: The list of tuples containing the document text and similarity score.
        """

        # Initialize the TF-IDF injector
        logger.info("Initializing the TF-IDF injector.")
        vectorizer = TfIdfInjector().get_vectorizer()
        #vectorizer = TfidfVectorizer()

        # Transform query to TF-IDF vector
        logger.info("Transforming the query to a TF-IDF vector.")
        query_vec = vectorizer.transform([query]).toarray()[0]

        # Connect to PostgreSQL
        logger.info("Connecting to PostgreSQL.")
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Query most similar documents using SQL cosine similarity
        logger.info("Querying the most similar documents using SQL cosine similarity.")
        cursor.execute("""
            SELECT document_text, 1 - (tfidf_vector <=> %s::vector) AS similarity
            FROM tf_idf_documents
            ORDER BY similarity DESC  -- Lower distance means higher similarity
            LIMIT %s
        """, (query_vec.tolist(), NUMBER_OF_MATCHES_FOR_TF_IDF))

        # Fetch results
        logger.info("Fetching results.")
        results = cursor.fetchall()

        # Close the cursor and connection
        logger.info("Closing the cursor and connection.")
        cursor.close()
        conn.close()

        return results


# Run retrieval
if __name__ == "__main__":
    sample_query = "to be conclusive an officer of that rank is not having due regard to the public service available notes 1 for definition of officer and courtmartial see s4 xxiii and xvi afa 2 the expression of the convening officers opinion justifying a departure from the general rules should be inserted in the convening order see form f2a sixth schedule to afr 3 see notes 4 and 5 to r 46 afr 4 this rule does not apply to sgcm see rl42 afr48 units of members of courtmartial a general or district courtmartial shall not be composed exclusively of officers of the same unit unless the convening officer states in the order convening the court that in his opinion other officers are not having due regard to the public service available and in no case shall it consist exclusively of officers belonging to the same unit as the accused notes 1 for definition of courtmartial officer and unit see s xvi xxiii and xxviii afa 2 the expression of the convening officers opinion justiying a departure from the general rule should be inserted in the convening order see form f 2 a sixth schedule to afr 3 see notes 4 and 5 to r46 afr 4 this rule does not apply to sgcm"
    top_docs = TfIdfRetrival().retrieve_relevant_docs(sample_query)

    print(top_docs)

    print("\nTop similar documents:")
    for doc, score in top_docs:
        print(f"Document: {doc} | Similarity Score: {score:.4f}")

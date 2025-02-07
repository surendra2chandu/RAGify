# Import necessary libraries , classes and functions
import psycopg2
from sklearn.feature_extraction.text import TfidfVectorizer
from src.conf.Configurations import db_config, NUMBER_OF_MATCHES_FOR_TF_IDF, logger
from src.utilities.DataBaseUtility import DataBaseUtility


def extract_docs(query: str):
    """
    Extracts documents similar to the query using TF-IDF.
    :param query: The query to search for.
    :return: The top similar documents.
    """


    # Fetch document content to build TF-IDF vocabulary
    logger.info("Fetching document content...")
    corpus = DataBaseUtility().extract_doc_content()

    # Compute TF-IDF vocabulary
    vectorizer = TfidfVectorizer()
    vectorizer.fit(corpus)

    # Transform query to TF-IDF vector
    query_vec = vectorizer.transform([query]).toarray()[0]

    # Connect to PostgreSQL
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Query most similar documents using SQL cosine similarity
    cursor.execute("""
        SELECT document_text, (tfidf_vector <=> %s::vector) AS similarity
        FROM documents
        ORDER BY similarity ASC  -- Lower distance means higher similarity
        LIMIT %s
    """, (query_vec.tolist(), NUMBER_OF_MATCHES_FOR_TF_IDF))

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return results


# Run retrieval
if __name__ == "__main__":
    sample_query = "How is artificial intelligence used in industries?"
    top_docs = extract_docs(sample_query)

    print("\nTop similar documents:")
    for doc, score in top_docs:
        print(f"Document: {doc} | Similarity Score: {score:.4f}")

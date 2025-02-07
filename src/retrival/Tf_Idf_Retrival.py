# Import necessary libraries , classes and functions
import psycopg2
from src.conf.Configurations import db_config, NUMBER_OF_MATCHES_FOR_TF_IDF, logger
from src.injestion.Tf_Idf_Injector import TfIdfInjector


def extract_docs(query: str):
    """
    Extracts documents similar to the query using TF-IDF.
    :param query: The query to search for.
    :return: The top similar documents.
    """

    # Initialize the TF-IDF injector
    logger.info("Initializing the TF-IDF injector.")
    vectorizer = TfIdfInjector().get_vectorizer()

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
        FROM documents
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
    sample_query = "air force life cycle management center standard process for life cycle sustainment plans lcsp process owner aflcmclg lz date 15 october 2020 version 7 0 1 record of changes record of changes version effective date summary 10 1 apr 2016 basic document approved by standard process sp board on 24 mar 16 20 1 jul 2016 updated to reflect afmccc delegation of sustainment command representative requirement for acat ii and below programs to center commanders 30 30 jul 2017 updated to reflect osd sample outline version 20 and other aflcmc level process improvements 40 1 oct 2017 administrative update to reflect updated afi 6310120 101 dtd 9 may 2017 reference changes"
    top_docs = extract_docs(sample_query)

    print("\nTop similar documents:")
    for doc, score in top_docs:
        print(f"Document: {doc} | Similarity Score: {score:.4f}")

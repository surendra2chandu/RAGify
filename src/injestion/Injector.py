# ingestion.py - Stores TF-IDF vectors in PostgreSQL

import psycopg2
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from src.conf.Configurations import db_config
from src.utilities.DataBaseUtility import DataBaseUtility


def store_tfidf_data():
    """Extracts documents, computes TF-IDF, and stores vectors in PostgreSQL."""

    # Fetch document content from database
    corpus = DataBaseUtility().extract_doc_content()

    # Compute TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus).toarray()  # Convert sparse matrix to dense

    # Connect to PostgreSQL
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("DROP TABLE IF EXISTS documents;")
    cursor.execute("""
        CREATE TABLE documents (
            id SERIAL PRIMARY KEY,
            document_text TEXT,
            tfidf_vector vector
        )
    """)

    # Insert each document and its vector
    for doc, vec in zip(corpus, tfidf_matrix):
        cursor.execute(
            "INSERT INTO documents (document_text, tfidf_vector) VALUES (%s, %s::vector)",
            (doc, vec.tolist())  # Convert NumPy array to list for PostgreSQL
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("TF-IDF vectors stored successfully.")


# Run ingestion
if __name__ == "__main__":
    store_tfidf_data()

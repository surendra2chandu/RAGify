# Importing necessary libraries
import psycopg2
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from src.conf.Configurations import db_config
from src.utilities.DataBaseUtility import DataBaseUtility

# Corpus (Documents)
corpus = DataBaseUtility().extract_doc_content()

# Initialize and Compute TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus).toarray()  # Convert sparse matrix to dense

# Store Data in PostgreSQL using `pgvector`
def store_tfidf_data(corpus, tfidf_matrix):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Drop and Create Table
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

# Perform Cosine Similarity in PostgreSQL
def extract_docs(query, top_n=2):
    """Finds the most similar documents using SQL-based cosine similarity."""
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Transform query to TF-IDF
    query_vec = vectorizer.transform([query]).toarray()[0]

    # Query to find most similar documents using cosine similarity
    cursor.execute("""
        SELECT document_text, (tfidf_vector <=> %s::vector) AS similarity
        FROM documents
        ORDER BY similarity ASC  -- Lower distance is more similar
        LIMIT %s
    """, (query_vec.tolist(), top_n))

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return results

# Store Data
store_tfidf_data(corpus, tfidf_matrix)

# Example Query
query = "How is artificial intelligence used in industries?"
top_docs = extract_docs(query)

print("\nTop 2 similar documents:")
for doc, score in top_docs:
    print(f"Document: {doc} | Similarity Score: {score:.4f}")

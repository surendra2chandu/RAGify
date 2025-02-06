# Importing necessary classes,libraries and modules
import psycopg2
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.conf.Configurations import db_config
from src.utilities.DataBaseUtility import DataBaseUtility

# Corpus (Documents)
corpus = DataBaseUtility().extract_doc_content()

# Initialize and Compute TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus).toarray()  # Convert sparse matrix to dense
feature_names = vectorizer.get_feature_names_out()  # Extract vocabulary (words)


# Display Word Matrix (TF-IDF)
df_tfidf = pd.DataFrame(tfidf_matrix, columns=feature_names, index=[f"Doc {i+1}" for i in range(len(corpus))])
print("\nTF-IDF Word Matrix:\n", df_tfidf)


# Store Data in PostgreSQL
def store_tfidf_data(corpus, tfidf_matrix):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Ensure table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            document_text TEXT,
            tfidf_vector FLOAT8[]
        )
    """)

    # Insert each document and its vector
    for doc, vec in zip(corpus, tfidf_matrix):
        cursor.execute(
            "INSERT INTO documents (document_text, tfidf_vector) VALUES (%s, %s)",
            (doc, vec.tolist())  # Convert NumPy array to list for storage
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("TF-IDF vectors stored successfully.")


# Fetch TF-IDF Data from PostgreSQL
def fetch_tfidf_data():
    """Fetches document texts and their stored TF-IDF vectors from the database."""
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT id, document_text, tfidf_vector FROM documents")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert retrieved data back to NumPy array
    doc_ids, documents, tfidf_vectors = [], [], []
    for row in rows:
        doc_ids.append(row[0])
        documents.append(row[1])
        tfidf_vectors.append(np.array(row[2]))  # Convert list back to NumPy array

    return doc_ids, documents, np.array(tfidf_vectors)


# Extract Top N Relevant Documents
def extract_docs(query, top_n=2):
    """Finds the most similar documents for a given query using cosine similarity."""
    query_vec = vectorizer.transform([query]).toarray()  # Transform query to TF-IDF
    doc_ids, documents, tfidf_vectors = fetch_tfidf_data()

    # Compute cosine similarity
    cosine_similarities = cosine_similarity(query_vec, tfidf_vectors).flatten()
    top_indices = np.argsort(cosine_similarities)[-top_n:][::-1]

    results = [(documents[i], cosine_similarities[i]) for i in top_indices]
    return results


# Store the corpus vectors in PostgreSQL
store_tfidf_data(corpus, tfidf_matrix)

# Example Query
query = "How is artificial intelligence used in industries?"
top_docs = extract_docs(query)

print("\nTop 2 similar documents:")
for doc, score in top_docs:
    print(f"Document: {doc} | Similarity: {score:.4f}")

from src.tf_idf.src.Data_files.corpus import documents
from src.tf_idf.src.query_implementing.query_vectorizer import DocumentSimilarity

#main function
if __name__ == "__main__":

    # Sample query
    sample = "adi narayana rao"

    # Initialize the DocumentSimilarity class
    document_similarity = DocumentSimilarity(documents)

    #top2_documents function is called
    document_similarity.top2_documents(sample)

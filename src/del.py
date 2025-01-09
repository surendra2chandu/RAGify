import spacy
from collections import defaultdict
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import os

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# Load SentenceTransformer model for embeddings
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def late_chunking_with_context(text):
    """Analyze the full text and extract meaningful chunks based on themes."""
    # Process the entire text
    doc = nlp(text)

    # Dictionaries to store chunks
    categories = defaultdict(list)

    # Analyze sentences for thematic grouping
    for sent in doc.sents:
        if "healthcare" in sent.text.lower() or "medical" in sent.text.lower():
            categories["Healthcare Applications"].append(sent.text)
        elif "finance" in sent.text.lower() or "risk" in sent.text.lower():
            categories["Financial Applications"].append(sent.text)
        elif "challenge" in sent.text.lower() or "ethical" in sent.text.lower():
            categories["Challenges in AI"].append(sent.text)
        else:
            categories["General Information"].append(sent.text)

    return categories

def generate_embeddings(chunks):
    """Generate embeddings for each chunk."""
    embeddings = {}
    for category, sentences in chunks.items():
        embeddings[category] = embedding_model.encode(sentences)
    return embeddings

def save_results_to_vector_database(embeddings, database_path="vector_db.txt"):
    """Save embeddings to a simple vector database (text file)."""
    with open(database_path, "w") as db:
        for category, vectors in embeddings.items():
            db.write(f"Category: {category}\n")
            for vector in vectors:
                db.write(f"{vector.tolist()}\n")

# Main function to process a PDF
def process_pdf(pdf_path, output_db_path="vector_db.txt"):
    # Step 1: Extract text from PDF
    text = extract_text_from_pdf(pdf_path)

    # Step 2: Perform late chunking
    chunks = late_chunking_with_context(text)

    # Step 3: Generate embeddings for chunks
    embeddings = generate_embeddings(chunks)

    # Step 4: Save embeddings to a vector database
    save_results_to_vector_database(embeddings, output_db_path)

    # Print categorized chunks
    for category, sentences in chunks.items():
        print(f"\n{category}:")
        for sentence in sentences:
            print(f"- {sentence}")

# Example usage
if __name__ == "__main__":
    pdf_file_path = "example.pdf"  # Replace with your PDF file path

    if os.path.exists(pdf_file_path):
        print("Processing PDF...")
        process_pdf(pdf_file_path)
        print("Results saved to vector database.")
    else:
        print(f"File {pdf_file_path} does not exist.")

import logging

# Set up logging configuration (Set the logging level to INFO)
logging.basicConfig(level=logging.INFO)

# Get the logger
logger = logging.getLogger()

# Define the chunk size
CHUNK_SIZE = 128

# Define the document type for PDF
DOC_TYPE_FOR_PDF  = "D"

# Define the document type for web data
DOC_TYPE_FOR_WEB = "W"

# Define the number of matches to return
NUMBER_OF_MATCHES = 3

# Define the URL for the LateChunking service
LATE_CHUNKING_URL = "http://127.0.0.1:8002/retrieve_text/"

# Define the URL for the Tf-Idf service
TF_IDF_URL = "http://127.0.0.1:8002/tf-idf/"

# Define the URL for the ollama service
OLLAMA_URL = "http://localhost:8001/llm/ollama/"

# Give the model path for MiniLM-L6-v2
model_path = r"C:\llm\MiniLM-L6-v2"

# Define the database configuration
db_config = {
        "dbname": "langchain",
        "user": "langchain",
        "password": "langchain",
        "host": "localhost",
        "port": 5432,
    }

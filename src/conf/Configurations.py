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
NUMBER_OF_MATCHES = 2

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
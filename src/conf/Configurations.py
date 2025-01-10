import logging

# Set up logging configuration (Set the logging level to INFO)
logging.basicConfig(level=logging.INFO)

# Get the logger
logger = logging.getLogger()

# Define the chunk size
CHUNK_SIZE = 128

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
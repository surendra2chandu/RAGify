
# Importing necessary classes
from fastapi import FastAPI
from src.routers.QueryVectorizerRouter import router as query_vectorizer_router

# Initialize the FastAPI app
app = FastAPI()

# Include the query vectorizer router
app.include_router(query_vectorizer_router)
# Importing necessary classes
from fastapi import FastAPI
from src.routers.QueryVectorizerRouter import router as query_vectorizer_router
from src.routers.SemanticRetrivalRouter import router as retrival_router
from src.routers.ChatBotRouter import router as chatbot_router

# Initialize the FastAPI app
app = FastAPI()

# Include the query vectorizer router
app.include_router(query_vectorizer_router)

# Include the retrival router
app.include_router(retrival_router)

# Include the chatbot router
app.include_router(chatbot_router)













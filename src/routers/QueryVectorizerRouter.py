# Import necessary libraries
from fastapi import APIRouter
from src.retrival.Retrival import QueryVectorizer

# Initialize the router
router = APIRouter(tags=["Similarities"])

# Define the route for the root endpoint
@router.post("/tf-idf/")
async def get_similar_docs(query: str):
    """
    Function to get response from the Tf-Idf service
    :param query: The query to be processed
    :return: The response from the service
    """

    # Get the top 2 most similar documents
    res = QueryVectorizer().extract_docs(query)

    # Return the response
    return res




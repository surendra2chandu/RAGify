# Importing necessary libraries
from fastapi import APIRouter
from src.retrival.DataRetrival import DataRetrival

# Initialize the router
router = APIRouter()


@router.post("/retrieve_text/")
async def retrieve_text(query: str):
    """
    This function retrieves relevant text based on the query.
    :param query: The query to search for.
    :return: The relevant text.
    """
    # Retrieve relevant text
    results = DataRetrival().retrieve_relevant_text(query)

    return results

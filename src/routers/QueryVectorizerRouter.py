from http.client import responses

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from src.conf.Configurations import logger
from src.tf_idf.QueryVectorizer import QueryVectorizer

# Initialize the router
router = APIRouter(tags=["Similarities"])

# Define the route for the root endpoint
@router.post("/tf-idf/")
async def get_similar_docs(query: str):

    # Get the top 2 most similar documents
    res = QueryVectorizer().top3_documents(query)

    # Prepare the response with line-by-line output
    # response = "\n".join([
    #     f"Sentence: '{corpus[doc]}' | Cosine similarity: {res['cosine_similarities'][doc]}"
    #     for doc in res["top_2_query"]
    # ])

    # response = []
    # for doc in res["top_2_query"]:
    #     response.append((corpus[doc], res["cosine_similarities"][doc]))

    return res




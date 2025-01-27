from http.client import responses

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from src.conf.Configurations import logger
from src.tf_idf.QueryVectorizer import QueryVectorizer

# Define the Pydantic model
class SimilarityRequest(BaseModel):
    corpus: List[str]
    query: str

# Initialize the router
router = APIRouter(tags=["Similarities"])

# Define the route for the root endpoint
@router.post("/tf-idf/")
async def get_similar_docs(request: SimilarityRequest):
    corpus = request.corpus
    query = request.query

    # Initialize the QueryVectorizer class with the corpus
    document_similarity = QueryVectorizer(corpus)

    # Get the top 2 most similar documents
    res = document_similarity.top2_documents(query)

    # Prepare the response with line-by-line output
    # response = "\n".join([
    #     f"Sentence: '{corpus[doc]}' | Cosine similarity: {res['cosine_similarities'][doc]}"
    #     for doc in res["top_2_query"]
    # ])

    response = ""
    for doc in res["top_2_query"]:
        response += corpus[doc]

    return response




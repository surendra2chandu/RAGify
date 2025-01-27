#import necessary libraries
import requests
from src.conf.Configurations import logger, TF_IDF_URL
from src.utilities.OllamaServiceManager import process_ollama_request


def get_response_tf_idf(query):
    """
    Function to get response from the Tf-Idf service
    :param query: The query to be processed
    :return: The response from the service
    """

    # Define the documents
    documents = [
        "The sun sets behind the mountains, casting a golden glow.",
        "The sun warmed the beach as we walked along the shore.",
        "She picked up her book and opened to the first page.",
        "After a long day, he relaxed with a hot cup of tea.",
        "The warmed air by the beach made the evening even more pleasant.",
        "Paris is the capital of France and efile tower is located in Paris."
    ]

    # Send a post request to the Tf-Idf service and get the response
    logger.info(f"Sending a post request to the Tf-Idf service with query: {query}")
    response = requests.post(TF_IDF_URL, json={"corpus": documents, "query": query})

    # Check the status code and get the response
    if response.status_code == 200:
        # Get the response in JSON
        response = response.json()

        for i in range(len(response)):
            if response[i][1] >= 0.2:
                # Process the response with the Ollama model
                logger.info("Processing the response with the Ollama model")
                response = process_ollama_request(response[i][0], query)
                break
        else:
            response = "No relevant information found in the database."

    else:
        response = f"Error occurred when processing the request to url {TF_IDF_URL}"

    # Return the response
    return response


if __name__ == "__main__":

    res = get_response_tf_idf("tell me about india?")

    print(res)

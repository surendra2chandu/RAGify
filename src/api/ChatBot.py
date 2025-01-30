#import necessary libraries
import requests
from src.conf.Configurations import logger, LATE_CHUNKING_URL, TF_IDF_URL
from src.utilities.OllamaServiceManager import process_ollama_request


def get_response(query):
    """
    Function to get response from the LateChunking service
    :param query: The query to be processed
    :return: The response from the service
    """
    # Initialize the context
    context = ""

    # Send a post request to the LateChunking service and get the response
    logger.info(f"Sending a post request to the LateChunking service with query: {query}")
    late_chunk_response = requests.post(LATE_CHUNKING_URL, params={"query": query})
    if late_chunk_response.status_code == 200:

        # Get the response in JSON format
        response = late_chunk_response.json()

        for i in range(len(response)):
            if response[i][1] >= 0.2:

                # Append the relevant information to the context
                logger.info(f"Appending relevant information to the context")
                context += response[i][0] + ". \n"

    else:
        response = f"Error occurred when processing the request to url {LATE_CHUNKING_URL}"

    # Send a post request to the Tf-Idf service and get the response
    logger.info(f"Sending a post request to the Tf-Idf service with query: {query}")
    tf_idf_response = requests.post(TF_IDF_URL, params={"query": query})

    # Check the status code and get the response
    if tf_idf_response.status_code == 200:
        # Get the response in JSON
        response = tf_idf_response.json()

        for i in range(len(response)):
            if response[i][1] >= 0.2:

                # Append the relevant information to the context
                logger.info(f"Appending relevant information to the context")
                context += response[i][0] + ". \n"
    else:
        response = f"Error occurred when processing the request to url {TF_IDF_URL}"

    if context:
        # Process the response with the Ollama model
        logger.info("Processing the response with the Ollama model")
        response = process_ollama_request(context, query)
    else:
        response = "No relevant information found in the database."

    # Return the response
    return response


if __name__ == "__main__":

    res = get_response("Who are the customers impacted by the upcoming satellite change for the AFN TV programming package in the Pacific region?")

    print(res)

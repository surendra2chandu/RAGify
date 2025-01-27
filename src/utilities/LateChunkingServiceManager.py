#import necessary libraries
import requests
from src.conf.Configurations import logger, LATE_CHUNKING_URL
from src.utilities.OllamaServiceManager import process_ollama_request


def get_response_late_chunking(query):
    """
    Function to get response from the LateChunking service
    :param query: The query to be processed
    :return: The response from the service
    """


    # Send a post request to the LateChunking service and get the response
    logger.info(f"Sending a post request to the LateChunking service with query: {query}")
    response = requests.post(LATE_CHUNKING_URL, params={"query": query})
    if response.status_code == 200:

        # Get the response in JSON format
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
        response = f"Error occurred when processing the request to url {LATE_CHUNKING_URL}"

    # Return the response
    return response


if __name__ == "__main__":

    res = get_response_late_chunking("Who are the customers impacted by the upcoming satellite change for the AFN TV programming package in the Pacific region?")

    print(res)

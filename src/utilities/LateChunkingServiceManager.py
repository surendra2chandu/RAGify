#import necessary libraries
import requests
from src.conf.Configurations import logger, LATE_CHUNKING_URL


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
        response = response.json()
    else:
        response = f"Error occurred when processing the request to url {LATE_CHUNKING_URL}"

    # Return the response
    return response


if __name__ == "__main__":

    res = get_response_late_chunking("sun?")

    print(res)

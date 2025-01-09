# Importing the required libraries
import requests
from bs4 import BeautifulSoup



def data_scraping_from_web(url):
    """
    This function fetches the content of a web page and prints the main content area.
    :param url: URL of the web page
    :return: Formatted content of the main content
    """

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'lxml')

        # Find the main content area
        content_div = soup.find('div', class_='mw-parser-output')

        if content_div:
            # Initialize a variable to store the formatted content
            formatted_output = ""

            # Loop through all children of the content div
            for element in content_div.find_all(['h1', 'h2', 'h3', 'p'], recursive=True):

                # If it's a heading
                if element.name in ['h1', 'h2', 'h3']:
                    formatted_output += f"\n\n{element.get_text(strip=True)}\n\n"

                # If it's a paragraph
                elif element.name == 'p':  # If it's a paragraph
                    formatted_output += f"{element.get_text(strip=True)}\n\n"

            # Return the formatted content
            return formatted_output
        else:
            print("Main content not found.")
    else:
        print(f"Failed to fetch the page. HTTP Status Code: {response.status_code}")


if __name__ == '__main__':

    # URL of the Wikipedia page
    sample_url = "https://en.wikipedia.org/wiki/Natural_language_processing#Natural_language_understanding"

    # Call the function with the URL
    result = data_scraping_from_web(sample_url)

    # print the result
    print(result)
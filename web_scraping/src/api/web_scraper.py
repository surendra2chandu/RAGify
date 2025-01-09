import requests
from web_scraping.src.utilities. data_extraction import get_data


def get_page_content(url):
    """
    This function takes a URL as an argument and returns the content of the page.
    :param url: URL of the page
    :return: content of the page
    """

    # Send an HTTP GET request to the specified URL and store the response in the variable 'r'
    response = requests.get(url=url)

    if response.status_code == 200:
        html_content = response.text

        result  = get_data(html_content)

        return result

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        exit()

if __name__ == "__main__":

    # URL of the Wikipedia page
    sample_url = " https://en.wikipedia.org/wiki/Natural_language_processing "

    # Call the method to get the content of the page
    res = get_page_content(sample_url)

    print(res)






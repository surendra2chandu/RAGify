import requests
from bs4 import BeautifulSoup


def get_links(url):

   # Send a GET request to fetch the HTML content of the page
   response = requests.get(url)

   # Check if the request was successful
   if response.status_code == 200:
      # Parse the HTML content using BeautifulSoup
      soup = BeautifulSoup(response.text, 'lxml')

      # Find the div with the specified class

      div_content = soup.find('div',class_ = 'feature-template-container')
      # Extract all anchor tags within the div
      if div_content:
          links = div_content.find_all('a')

          # Loop through and print the hrefs
          for link in links:
             href = link.get('href')
             if href:
                  return href
      else:
           print("Specified div is not there in page")

   else:
       print(f"Failed to fetch the page. HTTP Status Code: {response.status_code}")



if __name__ == "__main__":
    url_link="https://www.defense.gov/News/"
    result = get_links(url_link)
    print(result)
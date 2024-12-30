import requests
from bs4 import BeautifulSoup

# URL of the website
url = "https://www.defense.gov/news/"

# Fetch the content of the website
response = requests.get(url)

if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the specific <div> with the class "alist-inner alist-more-here"
    target_div = soup.find('div', class_="alist-inner alist-more-here")

    print("target dic", target_div)

    if target_div:
        # Extract child elements (e.g., titles, dates, summaries, links)
        for item in target_div.find_all('div', recursive=False):  # Assuming each child represents an article
            # Title
            title = item.find('a').text.strip() if item.find('a') else "No title found"
            # Date
            date = item.find('span', class_='date').text.strip() if item.find('span', class_='date') else "No date found"
            # Summary
            summary = item.find('p').text.strip() if item.find('p') else "No summary found"
            # Link
            link = item.find('a')['href'] if item.find('a') else "No link found"

            print(f"Title: {title}")
            print(f"Date: {date}")
            print(f"Summary: {summary}")
            print(f"Link: {link}")
            print("-" * 80)
    else:
        print("Target <div> not found on the page.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

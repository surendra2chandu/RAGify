import requests
from bs4 import BeautifulSoup

html_content = """<div class="alist-inner alist-more-here">
<feature-template :remove-grid="true" :show-all="true" template-mode="story">
<listing-with-preview :show-image="true" article-alt="Social media image for the Department of Defense website." article-id="4016543" article-image-url="" article-summary="Secretary of Defense Lloyd J. Austin III spoke by phone with his Turkish counterpart about the ongoing situation in Syria." article-title="Readout of Secretary of Defense Lloyd J. Austin III's Phone Call With Turkish Minister of National Defense Yaşar Güler" article-url="https://www.defense.gov/News/Releases/Release/Article/4016543/readout-of-secretary-of-defense-lloyd-j-austin-iiis-phone-call-with-turkish-min/" article-url-or-link="https://www.defense.gov/News/Releases/Release/Article/4016543/readout-of-secretary-of-defense-lloyd-j-austin-iiis-phone-call-with-turkish-min/" article-url-or-link-absolute="https://www.defense.gov/News/Releases/Release/Article/4016543/readout-of-secretary-of-defense-lloyd-j-austin-iiis-phone-call-with-turkish-min/" category="" content-type-name="News Release" content-type-val="9" image-caption="Social media image for the Department of Defense website." image-url="https://media.defense.gov/2021/Sep/30/2002865254/825/780/0/210930-D-EX074-055.JPG" item-index="1" open-in-new="" publish-date-ap="Dec. 24, 2024" publish-date-jss="2024-12-24T14:57:00" term-name="" term-url="">
</listing-with-preview>
</feature-template>
</div>"""

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all listing elements
listings = soup.find_all('listing-with-preview')

# Extract data
for listing in listings:
    content_type = listing.get('content-type-name', 'Unknown').strip()
    publish_date = listing.get('publish-date-ap', 'Unknown').strip()
    title = listing.get('article-title', 'Unknown').strip()
    summary = listing.get('article-summary', 'Unknown').strip()
    article_url = listing.get('article-url', 'Unknown').strip()

    print(f"{content_type} | {publish_date}")
    print(f"{title}")
    print(f"{summary}")
    print(f"URL: {article_url}")

    # Now fetch the article URL content
    if article_url != 'Unknown':
        try:
            # Fetch the content of the article
            response = requests.get(article_url)
            article_soup = BeautifulSoup(response.text, 'html.parser')

            print(article_soup)

            # Example: Get the first paragraph (you can customize this based on your needs)
            article_paragraph = article_soup.find('p') # You can adjust this based on the actual article structure
            if article_paragraph:
                print(f"Article Content: {article_paragraph.text.strip()}")
            else:
                print("No content found in the article.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch article content: {e}")
    print()  # Add a line break between entries

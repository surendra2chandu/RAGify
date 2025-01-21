import requests
from bs4 import BeautifulSoup

html_content = """<div class="alist-inner alist-more-here">
<feature-template :remove-grid="true" :show-all="true" template-mode="story">
<listing-with-preview :show-image="true" article-alt="A man in a uniform poses for a photo." article-id="4014615" article-image-url="https://media.defense.gov/2024/Dec/20/2003617742/825/780/0/241220-A-D0439-0082M.JPG" article-summary="Army Col. Robert Lewis Howard is the most decorated soldier to have served in the Vietnam War and is the only soldier to have been nominated three times for the Medal of Honor." article-title="Medal of Honor Monday: Army Col. Robert L. Howard" article-url="https://www.defense.gov/News/Feature-Stories/Story/Article/4014615/medal-of-honor-monday-army-col-robert-l-howard/" article-url-or-link="https://www.defense.gov/News/Feature-Stories/Story/Article/4014615/medal-of-honor-monday-army-col-robert-l-howard/" article-url-or-link-absolute="https://www.defense.gov/News/Feature-Stories/Story/Article/4014615/medal-of-honor-monday-army-col-robert-l-howard/" category="" content-type-name="Story" content-type-val="800" image-caption="Social media image for the Department of Defense website." image-url="https://media.defense.gov/2024/Dec/20/2003617742/825/780/0/241220-A-D0439-0082M.JPG" item-index="1" open-in-new="" publish-date-ap="Dec. 30, 2024" publish-date-jss="2024-12-30T07:37:17" term-name="" term-url="">
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
    print(f"URL: {article_url}" )

    # Now fetch the article URL content
    if article_url != 'Unknown':
        try:
            # Fetch the content of the article
            response = requests.get(article_url)
            article_soup = BeautifulSoup(response.text, 'html.parser')

            #print(article_soup)

            # Example: Get the first paragraph (you can customize this based on your needs)
            article_paragraph = article_soup.find('p')
            if article_paragraph:
                print(f"Article Content: {article_paragraph.text.strip()}")
            else:
                print("No content found in the article.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch article content: {e}")
    print()
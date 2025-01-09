from bs4 import BeautifulSoup

def get_data(text):
    """
    This function takes the text of the page as an argument and returns the data extracted from the page.
    :param text: raw text of the page
    :return: extracted data
    """

    # Beautifulsoup is a get the data from the response and parse it
    soup = BeautifulSoup(text, "lxml")

    # Use the BeautifulSoup object 'soup' to find the first <span> element(Heading)
    article = soup.find("span", {"class": "mw-page-title-main"})
    print(article.text + " :- ")

    tags = soup.find("p")
    # print(tags)

    # we will take the empty list and append the text of the tags
    text_formate = []

    # you get the text of the tags and append it to the list using the for loop
    for tag in tags:
        i = tag.text
        text_formate.append(i)

    # print the text of the tags
    print(tags.text)


    article2 = soup.find("h2", id="History")

    all_paragraphs = soup.find_all("p")

    history_part = all_paragraphs[2]
    head = soup.find("div", class_="mw-heading mw-heading3")
    sub = all_paragraphs[3]
    result = article2.text + " :- ", history_part.text, " \n " + head.text + " :-", " \n  " + sub.text

    return result

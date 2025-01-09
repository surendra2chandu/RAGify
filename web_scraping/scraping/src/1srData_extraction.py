from http.client import responses

import requests
from bs4 import BeautifulSoup
def link_to_data(url):
    response=requests.get(url)
    soup=BeautifulSoup(response.text, "lxml")
    para=soup.find("div",class_="body")
    return para



if __name__ == "__main__":
    sample_url="https://www.defense.gov/News/Releases/Release/Article/4016543/readout-of-secretary-of-defense-lloyd-j-austin-iiis-phone-call-with-turkish-min/"
    res=link_to_data(sample_url)
    print(res.text)
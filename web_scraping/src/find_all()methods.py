
import pandas as pd
import requests
from bs4 import BeautifulSoup
url="https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets"
r=requests.get(url)
soup=BeautifulSoup(r.text,"lxml")
#print(soup)

names=soup.find_all("a",class_="title")
#print(names)
product_name=[]
for i in names:
  name=i.text
  product_name.append(name)
#print(product_name)

prices=soup.find_all("h4",class_="price float-end card-title pull-right")
#print(prices)
prices_list=[]
for i in prices:
  price=i.text
  prices_list.append(price)
#print(prices_list)

desc=soup.find_all("p",class_="description")
#print(desc)
desc_list=[]
for i in desc:
  description=i.text
  desc_list.append(description)
#print(desc_list)

reviews=soup.find_all("p",class_="review-count float-end")
#print(reviews)
review_list=[]
for i in reviews:
    review=i.text
    review_list.append(review)
#print(reviews)

# Create Dataframe
data=pd.DataFrame({"Product Name":product_name,"Price":prices_list,"Description":desc_list,"Reviews":reviews})
#print(data)
data.to_csv("computers.csv")

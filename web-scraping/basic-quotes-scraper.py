# https://www.youtube.com/watch?v=QhD015WUMxE&ab_channel=Tinkernut
# https://medium.com/@kshamasinghal/scraping-quotes-to-scrape-website-using-python-c8a616b244e7
# https://stackoverflow.com/questions/74740511/how-to-perform-paging-to-scrape-quotes-over-several-pages

from bs4 import BeautifulSoup
import requests
import pandas as pd

page = requests.get('https://quotes.toscrape.com/')
soup = BeautifulSoup(page.text, 'html.parser')

quotes = soup.find_all("span", attrs={"class": "text"})
authors = soup.find_all("small", attrs={"class": "author"})
tags = soup.find_all("div", attrs={"class": "tags"})

quotes_dict = []
for (quote, author, tag) in zip(quotes, authors, tags): 
    quotes_dict.append({'quote': quote.text, 'author': author.text, 'tags': tag.meta['content']})

quotes_df = pd.DataFrame(quotes_dict)
quotes_df.to_csv('quotes.csv',index=None)





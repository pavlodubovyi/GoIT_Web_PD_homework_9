import requests
from bs4 import BeautifulSoup

url = 'https://quotes.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
quotes = soup.find_all('span', class_='text')
authors = soup.find_all('small', class_='author')
tags = soup.find_all('div', class_='tags')


def to_json(quotes, authors, tags):
    for i in range(2):
        print(quotes[i].text)
        print(authors[i].text)
        tagsforquote = tags[i].find_all('a', class_='tag')
        for tagf in tagsforquote:
            print(tagf.text)

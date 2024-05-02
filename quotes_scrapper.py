import requests
from bs4 import BeautifulSoup
import json


def get_page_content(url):
    response = requests.get(url)
    content = BeautifulSoup(response.content, 'html.parser')
    return content


def get_quotes(content):
    quotes = content.find_all('div', class_='quote')
    quotes_list = []
    for quote in quotes:
        quote_info = {
            "tags": [tag.text for tag in quote.find_all('a', class_='tag')],
            "author": quote.find('small', class_='author').get_text(),
            "quote": quote.find('span', class_='text').get_text()
        }
        quotes_list.append(quote_info)
    return quotes_list


def get_authors(content):
    authors = content.find_all('div', class_='quote')
    authors_list = []
    for author in authors:
        author_info = {
            "fullname": author.find('small', class_='author').get_text(),
            "born_date": author.find('span', class_='author-born-date').get_text() if author.find('span', class_='author-born-date') else "",
            "born_location": author.find('span', class_='author-born-location').get_text() if author.find('span', class_='author-born-location') else "",
            "description": author.find('div', class_='author-description').get_text() if author.find('div', class_='author-description') else ""
        }
        authors_list.append(author_info)
    return authors_list


def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    BASE_URL = 'http://quotes.toscrape.com'
    page_content = get_page_content(BASE_URL)

    the_authors = []

    while True:
        the_authors.extend(get_authors(page_content))

        next_page_link = page_content.find('li', class_='next')
        if next_page_link is None:
            break

        next_page_url = BASE_URL + next_page_link.find('a')['href']
        page_content = get_page_content(next_page_url)

    save_to_json(the_authors, 'authors.json')

    # Отримання цитат і їх збереження у файл
    quotes = get_quotes(page_content)
    save_to_json(quotes, 'quotes.json')


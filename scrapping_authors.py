import requests
from bs4 import BeautifulSoup
import json

url = "https://quotes.toscrape.com/"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

# Find all 'a' tags with href containing '/author/'
author_links = soup.find_all('a', href=lambda href: href and '/author/' in href)

# Filter 'a' tags containing '(about)'
about_links = [link['href'] for link in author_links if '(about)' in link.text]

print(about_links)
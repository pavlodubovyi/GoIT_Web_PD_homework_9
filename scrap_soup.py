import requests
from bs4 import BeautifulSoup


url = "https://quotes.toscrape.com/"
page = requests.get(url)
soup = BeautifulSoup(page.text, "lxml")
# quotes = soup.find_all("span", class_="text")
# authors = soup.find_all("small", class_="author")
# tags = soup.find_all("div", class_="tags")
#
# for i in range(len(quotes)):
#     print(quotes[i].text)
#     print("---" + authors[i].text + "---")
#     tags_in_quotes = tags[i].find_all("a", class_="tag")
#     for t in tags_in_quotes:
#         print(t.text)

# знайти перший тег <p> на сторінці
first_paragraph = soup.find("p")
body_children = list(first_paragraph.children)
print(body_children)

all_paragraphs = soup.find_all("p")
print(all_paragraphs)


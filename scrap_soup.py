import requests
from bs4 import BeautifulSoup
import json
from models import Quote, Author
import os.path

BASE_URL = "https://quotes.toscrape.com/"


def manage_quotes():
    page = requests.get(BASE_URL)
    soup = BeautifulSoup(page.content, "lxml")

    # Extract quotes, authors and tags
    quotes = soup.find_all("span", class_="text")
    authors = soup.find_all("small", class_="author")
    tags = soup.find_all("div", class_="tags")

    # Creating list to store quotesdata
    data_quotes = []

    # Add data to quotes.json lists:
    if not os.path.exists("quotes.json"):
        with open("quotes.json", "r", encoding="utf-8") as q:
            json.load(q)

    for i in range(len(quotes)):
        quote_text = quotes[i].text
        author_name = authors[i].text
        tags_in_quotes = [t.text for t in tags[i].find_all("a", class_="tag")]

        data_quotes.append({
            "tags": tags_in_quotes,
            "author": author_name,
            "quote": quote_text
        })

    with open("quotes.json", "w", encoding="utf-8") as quotes_file:
        json.dump(data_quotes, quotes_file, indent=2)
    print("Quotes saved to quotes.json")


# Dealing with authors
def manage_authors():
    page = requests.get(BASE_URL)
    soup = BeautifulSoup(page.content, "lxml")

    # Extract author links
    author_links = soup.find_all("a", href=lambda href: href and "/author/" in href)
    about_links = [link["href"] for link in author_links if "(about)" in link.text]

    authors = []

    # Function to check if an author already exists in authors.json
    def author_exists(fullname, auth):
        for author in auth:
            if author["fullname"] == fullname:
                return True
        return False

    # Check if authors.json file exists
    if os.path.exists("authors.json"):
        # Read existing authors from the file
        with open("authors.json", 'r') as f:
            authors = json.load(f)

    for ur in about_links:
        url = BASE_URL + ur
        response = requests.get(url)
        print(f"Managing {url}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "lxml")

            # Extract author info
            author_name = soup.find("h3", class_="author-title").text
            author_born = soup.find("span", class_="author-born-date").text
            author_born_location = soup.find("span", class_="author-born-location").text.strip(" in ")
            author_description = soup.find("div", class_="author-description").text.lstrip()

            if not author_exists(author_name, authors):
                authors_info = {
                    "fullname": author_name,
                    "born_date": author_born,
                    "born_location": author_born_location,
                    "description": author_description
                }
                authors.append(authors_info)
        else:
            print(f"Unable to get response: Status {response.status_code} - {url}")

    # Add data to authors.json lists:
    with open("authors.json", "w", encoding="utf-8") as authors_file:
        json.dump(authors, authors_file, indent=2)


if __name__ == "__main__":
    manage_quotes()
    manage_authors()

import requests
from bs4 import BeautifulSoup
import json
import datetime
import os.path

BASE_URL = "https://quotes.toscrape.com/"


def manage_quotes(url):
    quotes_data = []
    if os.path.exists("quotes.json"):
        with open("quotes.json", "r", encoding="utf-8") as q:
            quotes_data = json.load(q)

    web_page = requests.get(url)
    soup = BeautifulSoup(web_page.content, "lxml")

    # Extract quotes, authors and tags
    quotes = soup.find_all("span", class_="text")
    authors = soup.find_all("small", class_="author")
    tags = soup.find_all("div", class_="tags")

    for i in range(len(quotes)):
        quote_text = quotes[i].text
        author_name = authors[i].text
        tags_in_quotes = [t.text for t in tags[i].find_all("a", class_="tag")]

        # Check if the quote is already in quotes.json
        if {"quote": quote_text, "author": author_name} not in quotes_data:
            quotes_data.append({
                "tags": tags_in_quotes,
                "author": author_name,
                "quote": quote_text
            })

            # Write updated quotes to quotes.json
            with open("quotes.json", "w", encoding="utf-8") as q:
                json.dump(quotes_data, q, indent=2)
            print(f"A quote of {author_name} added to quotes.json")
    return quotes_data


# Dealing with authors
def manage_authors(url):
    web_page = requests.get(url)
    soup = BeautifulSoup(web_page.content, "lxml")

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

                # Write updated authors to the file
                with open("authors.json", 'w') as af:
                    json.dump(authors, af, indent=2)
                print(f"Info about {author_name} added to authors.json")
        else:
            print(f"Unable to get response: Status {response.status_code} - {url}")
    return authors


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    data_quotes = []
    authors_data = []

    page_url = BASE_URL
    while True:
        page = requests.get(page_url)
        if page.status_code == 200:
            print(f"Managing {page_url}")
            data_quotes += manage_quotes(page_url)
            authors_data += manage_authors(page_url)
            next_button = BeautifulSoup(page.content, "html.parser").find("li", class_="next")
            if next_button:
                next_url = next_button.find("a")["href"]
                page_url = BASE_URL + next_url
            else:
                break
        else:
            break

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print(f"Scraping completed in {duration}. I'd better try Scrappy :)")

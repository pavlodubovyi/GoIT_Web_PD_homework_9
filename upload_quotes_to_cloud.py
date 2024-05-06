"""
Цей скрипт завантажує json файли у хмарну базу даних
"""
import json

from mongoengine.errors import NotUniqueError

from models import Author, Quote

if __name__ == "__main__":
    with open("authors.json", encoding="utf-8") as file_descriptor:
        data = json.load(file_descriptor)
        for el in data:
            try:
                author = Author(fullname=el.get("fullname"), born_date=el.get("born_date"),
                                born_location=el.get("born_location"), description=el.get("description"))
                author.save()
            except NotUniqueError:
                print(f"Author already exists {el.get('fullname')}")

    with open("quotes.json", encoding="utf-8") as fd:
        data = json.load(fd)
        for el in data:
            author_name = el.get("author").replace("-", " ")
            authors = Author.objects(fullname=el.get("author"))
            if authors:
                author = authors[0]
                quote = Quote(quote=el.get("quote"), tags=el.get("tags"), author=author)
                quote.save()
            else:
                print(f"No author found for quote {el.get('quote')}")

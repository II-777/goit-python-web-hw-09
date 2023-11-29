from pymongo import MongoClient
from mongoengine import connect
from models import Authors, Quotes
import json
from datetime import datetime


def LoadData():
    cluster = MongoClient(
        "mongodb+srv://II-777:1234@cluster0.u2illjh.mongodb.net/?retryWrites=true&w=majority")
    db = cluster["hw08"]
    connect(db="hw08", alias="default",
            host="mongodb+srv://II-777:1234@cluster0.u2illjh.mongodb.net/?retryWrites=true&w=majority")

    with open('authors.json', 'r', encoding='utf-8') as file:
        authors_data = json.load(file)

    for author_data in authors_data:
        born_date = datetime.strptime(author_data['born_date'], '%B %d, %Y')
        author = Authors(
            fullname=author_data['fullname'],
            born_date=born_date,
            born_location=author_data['born_location'],
            description=author_data['description']
        )
        author.save()

    with open('quotes.json', 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)

    for quote_data in quotes_data:
        author = Authors.objects(fullname=quote_data['author']).first()
        quote = Quotes(
            tags=quote_data['tags'],
            author=author,
            quote=quote_data['quote']
        )
        quote.save()


if __name__ == "__main__":
    LoadData()
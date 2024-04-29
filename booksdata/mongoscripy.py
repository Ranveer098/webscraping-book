from pymongo import MongoClient
import datetime

client = MongoClient("mongodb+srv://admin:admin123@cluster0.jbd81tu.mongodb.net/")
db = client.scrapydb
collection = db.books

post = {
    "author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.now(tz=datetime.timezone.utc),
}

post_id = collection.insert_one(post).inserted_id

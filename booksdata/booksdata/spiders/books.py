import scrapy
from pathlib import Path
from pymongo import MongoClient
import datetime

client = MongoClient("mongodb+srv://admin:admin123@cluster0.jbd81tu.mongodb.net/")
db = client.scrapydb
collection = db.books

def insertDb(page, title, rating, image, price, stock):
    collection = db[page]
    doc = {
        "title": title,
        "rating": rating,
        "image": image,
        "price": price,
        "stock": stock,
        "date": datetime.datetime.now()
    }
    inserted = collection.insert_one(doc)
    return inserted.inserted_id

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]

    def start_requests(self):
        urls = [
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"books-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
        cards = response.css(".product_pod")
        for card in cards:
            title = card.css("h3 > a::text").get()
            rating = card.css(".star-rating::attr(class)").get().split()[-1]
            image = card.css(".image_container img::attr(src)").get().replace("../../../../media", "https://books.toscrape.com/media")
            price = card.css(".price_color::text").get()
            if len(card.css(".availability .icon-ok")) > 0:
                stock = True
            else:
                stock = False
            
            insertDb(page, title, rating, image, price, stock)

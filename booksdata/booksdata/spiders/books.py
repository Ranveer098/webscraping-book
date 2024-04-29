import scrapy
from pathlib import Path


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
        bookdetails={}

        self.log(f"Saved file {filename}")
        cards=response.css(".product_pod")
        for card in cards:
            title=card.css("h3>a::text").get()
            print(title)
            rating=card.css(".star-rating").attrib["class"].split(" ")[1]
            print(rating)
            image=card.css(".image_container img").attrib["src"]
            print(image)
            price=card.css(".price_color::text").get()
            print(price)
            availability = card.css(".availability::text").get()
            if len(card.css(".availability .icon-ok")) > 0:
              stock = True
            else:
             stock = False
         
       
        

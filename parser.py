import scrapy


class WebsiteSpider(scrapy.Spider):
    name = "website_spider"
    start_urls = ["http://megainvest.com.ua/strojmaterialy/"]

    def parse(self, response):
        categories = response.css(".inav a")
        for category in categories:
            category_name = category.css("::text").get()
            category_url = category.css("::attr(href)").get()
            yield scrapy.Request(url=category_url, callback=self.parse_category, meta={"category": category_name})

    def parse_category(self, response):
        category = response.meta["category"]
        products = response.css(".product-thumb")
        for product in products:
            product_name = product.css("::text").get().strip()
            yield {"Category": category, "Product": product_name}


# Запуск парсера
from scrapy.crawler import CrawlerProcess

output_filename = "res.csv"
process = CrawlerProcess()
process.crawl(WebsiteSpider)
process.start()
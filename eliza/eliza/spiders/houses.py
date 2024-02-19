import scrapy


class HousesSpider(scrapy.Spider):
    name = "houses"
    allowed_domains = ["www.immoweb.be"]
    start_urls = ["https://www.immoweb.be/en/search/house/"]

    def start_requests(self):
        URL = 'https://www.immoweb.be/en/search/house/'
        yield scrapy.Request(url=URL, callback=self.response_parser)

    def response_parser(self, response):
        for selector in response.css("article.search-results__item"):
            yield {
                ""
            }

    def parse(self, response):
        pass

#This is not  finished
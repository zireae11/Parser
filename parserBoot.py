import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CrawlingSpider(CrawlSpider):
    name = "practica"
    allowed_domains = ["i-hls.com"]
    start_urls = ["https://i-hls.com/"]

    rules = (
        Rule(LinkExtractor(allow="iHLS/news/")),
        Rule(LinkExtractor(allow="iHLS", deny="news"), callback="parse_item"),
    )

    def parse_item(self, response):
        title = response.css(".entry-title a::text").get()
        date = response.css(".meta-info time::text").get()
        page_text = response.css(".td-post-text-excerpt::text").get()

        data = {
            'title': title,
            'date': date,
            'page_text': page_text
        }

        yield data


# Запуск краулинга и запись данных в файл JSON
filename = 'output.json'

process = scrapy.crawler.CrawlerProcess(settings={
    'FEEDS': {filename: {'format': 'json'}},
    'LOG_ENABLED': False
})

process.crawl(CrawlingSpider)
process.start()

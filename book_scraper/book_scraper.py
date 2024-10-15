import scrapy
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.log import configure_logging

class BookSpider(scrapy.Spider):
    name = 'book_spider'
    start_urls = ['https://www.3anet.co.jp/data/4030/?detailFlg=0']

    def parse(self, response):
        book_info = response.css('div.iteminfo-area')
        if book_info:
            title = book_info.css('h2.book-title::text').get().strip()
            description = book_info.css('div.about-feature::text').get().strip()
            toc = book_info.css('p.index-list::text').get().strip()

            yield {
                'title': title,
                'description': description,
                'table_of_contents': toc
            }
        else:
            self.logger.warning("No book information found.")

def run_spider():
    configure_logging()
    runner = CrawlerRunner()
    d = runner.crawl(BookSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

if __name__ == "__main__":
    run_spider()
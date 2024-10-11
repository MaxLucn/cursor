import scrapy
from book_spider.items import BookItem


class BookSpider(scrapy.Spider):
    name = 'book_spider'
    start_urls = ['https://www.3anet.co.jp/np/books/4030/']

    target_books = [
        '小論文への１２のステップ',
        '入社1年目ビジネスマナー教科書',
        '日本語上級話者 への道 きちんと伝える技術と表現',
        '外国人のための ケーススタディで学ぶビジネス日本語 中級'
    ]

    def parse(self, response):
        self.logger.info(f"Parsing page: {response.url}")

        all_h2 = response.xpath('//h2/text()').getall()
        self.logger.info(f"All h2 elements: {all_h2}")

        for book_title in self.target_books:
            self.logger.info(f"Searching for book: {book_title}")
            book = response.xpath(f'//*[contains(text(), "{book_title}")]/..')
            if book:
                self.logger.info(f"Found book: {book_title}")
                item = BookItem()
                item['title'] = book_title
                item['author'] = book.xpath('.//p[@class="author"]/text()').get().strip()
                item['price'] = book.xpath('.//p[@class="price"]/text()').get().strip()
                item['isbn'] = book.xpath('.//p[@class="isbn"]/text()').get().strip()

                # 查找"立ち読み"按钮的链接
                preview_url = book.xpath('.//a[contains(@class, "btn_preview")]/@href').get()
                if preview_url:
                    yield scrapy.Request(response.urljoin(preview_url), callback=self.parse_preview,
                                         meta={'item': item})
                else:
                    self.logger.warning(f"Preview link not found for book: {book_title}")
            else:
                self.logger.warning(f"Book not found: {book_title}")

    def parse_preview(self, response):
        item = response.meta['item']

        # 提取试读内容
        preview_content = response.xpath('//div[@class="preview-content"]//text()').getall()
        item['preview'] = '\n'.join([content.strip() for content in preview_content if content.strip()])

        self.logger.info(f"Extracted preview for book: {item['title']}")
        yield item
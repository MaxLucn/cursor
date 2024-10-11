import scrapy

class BookItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    isbn = scrapy.Field()
    description = scrapy.Field()
    table_of_contents = scrapy.Field()
    preview = scrapy.Field()
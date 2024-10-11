BOT_NAME = 'book_spider'

SPIDER_MODULES = ['book_spider.spiders']
NEWSPIDER_MODULE = 'book_spider.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
   'book_spider.pipelines.BookPipeline': 300,
}

# 设置文件下载路径
FILES_STORE = 'scraped_data'
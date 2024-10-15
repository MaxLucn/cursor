BOT_NAME = 'book_spider'

SPIDER_MODULES = ['book_spider.spiders']
NEWSPIDER_MODULE = 'book_spider.spiders'

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
   'book_spider.pipelines.BookPipeline': 300,
}

# 允许下载大文件
DOWNLOAD_WARNSIZE = 0
DOWNLOAD_MAXSIZE = 0

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

DOWNLOAD_DELAY = 2
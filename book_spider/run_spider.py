import os
import sys

# 打印当前工作目录
print("Current working directory:", os.getcwd())

# 将当前文件的父目录添加到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# 打印 Python 路径
print("Python path:", sys.path)

try:
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings
    from book_spider.spiders.book_spider import BookSpider
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(BookSpider)
    process.start()

if __name__ == '__main__':
    run_spider()
import scrapy
import io
from PyPDF2 import PdfReader
import requests


class BookSpider(scrapy.Spider):
    name = 'book_spider'
    start_urls = ['https://www.3anet.co.jp/data/4030/?detailFlg=0']

    def parse(self, response):
        self.logger.info(f"Parsing page: {response.url}")

        # 查找所有可能的PDF链接
        pdf_links = response.css('a[href$=".pdf"]::attr(href)').getall()

        if pdf_links:
            for pdf_link in pdf_links:
                yield scrapy.Request(url=response.urljoin(pdf_link), callback=self.parse_pdf)
        else:
            self.logger.warning("No PDF links found on the page.")

    def parse_pdf(self, response):
        self.logger.info(f"Processing PDF: {response.url}")

        # 检查是否是PDF文件
        if 'application/pdf' in response.headers.get('Content-Type', b'').decode('utf-8'):
            # 保存PDF文件
            filename = response.url.split('/')[-1]
            pdf_path = f'scraped_books/{filename}'
            with open(pdf_path, 'wb') as f:
                f.write(response.body)
            self.logger.info(f"Saved PDF: {pdf_path}")

            # 提取PDF文本
            try:
                reader = PdfReader(io.BytesIO(response.body))
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"

                # 保存提取的文本
                txt_filename = pdf_path.replace('.pdf', '.txt')
                with open(txt_filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                self.logger.info(f"Saved text: {txt_filename}")

                yield {
                    'pdf_url': response.url,
                    'pdf_file': pdf_path,
                    'text_file': txt_filename
                }
            except Exception as e:
                self.logger.error(f"Error extracting text from PDF: {e}")
        else:
            self.logger.warning(f"The response is not a PDF file: {response.url}")
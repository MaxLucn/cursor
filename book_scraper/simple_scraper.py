import os
import sys
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

print("Script started")


def setup_driver():
    print("Setting up driver")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("Driver setup complete")
    return driver


def wait_for_pdf_viewer(driver, timeout=120):
    print("Waiting for PDF viewer to load...")
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return window.PDFViewerApplication && window.PDFViewerApplication.pdfDocument")
        )
        print("PDF viewer loaded successfully")
        return True
    except:
        print("Timeout waiting for PDF viewer to load")
        return False


def scrape_book_info(url):
    print(f"Scraping URL: {url}")
    driver = setup_driver()
    driver.get(url)

    try:
        print("Waiting for page to load")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(10)

        print("Page loaded, searching for iframe")
        iframe = driver.find_element(By.TAG_NAME, 'iframe')
        if iframe:
            iframe_src = iframe.get_attribute('src')
            print(f"Iframe found, src: {iframe_src}")

            # Switch to iframe
            driver.switch_to.frame(iframe)

            # Wait for iframe content to load
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Try to extract content directly from iframe
            iframe_content = driver.find_element(By.TAG_NAME, 'body').text
            print(f"Iframe content (first 500 characters): {iframe_content[:500]}")

            # Switch back to default content
            driver.switch_to.default_content()

            # Now try to access PDF viewer
            pdf_viewer_url = f"{iframe_src}pdfViewer/"
            print(f"Accessing PDF viewer URL: {pdf_viewer_url}")
            driver.get(pdf_viewer_url)

            if not wait_for_pdf_viewer(driver):
                print("Failed to load PDF viewer")
                return

            # Use JavaScript to get book info and content
            book_info = driver.execute_script("""
                return {
                    title: document.title,
                    totalPages: window.PDFViewerApplication.pagesCount,
                };
            """)

            title = book_info['title']
            total_pages = book_info['totalPages']
            print(f"Book title: {title}")
            print(f"Total pages: {total_pages}")

            all_content = f"Title: {title}\n\n"
            all_content += f"Iframe content:\n{iframe_content}\n\n"

            for page in range(1, total_pages + 1):
                print(f"Scraping page {page}")
                page_content = driver.execute_script(f"""
                    return window.PDFViewerApplication.pdfDocument.getPage({page}).then(function(page) {{
                        return page.getTextContent().then(function(textContent) {{
                            return textContent.items.map(function(item) {{ return item.str; }}).join(' ');
                        }});
                    }});
                """)
                all_content += f"\nPage {page}:\n{page_content}\n"

            filename = f"scraped_books/{title.replace(' ', '_')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(all_content)
            print(f"Saved all content to {filename}")

        else:
            print("No iframe found")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Traceback:")
        traceback.print_exc()

    finally:
        driver.quit()
        print("Driver closed")


if __name__ == "__main__":
    url = "https://www.3anet.co.jp/data/4030/?detailFlg=0"
    scrape_book_info(url)
    print("Scraping completed")
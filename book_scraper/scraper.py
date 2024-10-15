import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    print(f"Created folder: {folder_name}")


def save_to_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved file: {filename}")


def scrape_book_info(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        print(f"Page title: {driver.title}")

        # Wait for the page to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Find the book element
        book = driver.find_element(By.CLASS_NAME, "iteminfo-area")

        # Extract book information
        title = book.find_element(By.CLASS_NAME, "book-title").text.strip()
        content = f"Title: {title}\n"

        # Try to find author, price, and ISBN
        try:
            author = book.find_element(By.CLASS_NAME, "author").text.strip()
            content += f"Author: {author}\n"
        except NoSuchElementException:
            print("Author not found")

        try:
            price = book.find_element(By.CLASS_NAME, "price").text.strip()
            content += f"Price: {price}\n"
        except NoSuchElementException:
            print("Price not found")

        try:
            isbn = book.find_element(By.CLASS_NAME, "isbn").text.strip()
            content += f"ISBN: {isbn}\n"
        except NoSuchElementException:
            print("ISBN not found")

        # Extract description
        try:
            description = book.find_element(By.CLASS_NAME, "about-feature").text.strip()
            content += f"\nDescription:\n{description}\n"
        except NoSuchElementException:
            print("Description not found")

        # Extract table of contents
        try:
            toc = book.find_element(By.CLASS_NAME, "index-list").text.strip()
            content += f"\nTable of Contents:\n{toc}\n"
        except NoSuchElementException:
            print("Table of Contents not found")

        # Save to file
        filename = f"scraped_books/{title.replace(' ', '_').replace('/', '_')}.txt"
        save_to_file(filename, content)

        print(f"Scraped and saved: {title}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()


if __name__ == "__main__":
    url = "https://www.3anet.co.jp/np/books/4030/"
    scrape_book_info(url)
    print("Scraping completed.")
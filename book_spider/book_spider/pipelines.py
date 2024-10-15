import os
import json


class BookPipeline:
    def process_item(self, item, spider):
        directory = 'scraped_books'
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = f"{directory}/{item['title'].replace(' ', '_')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Title: {item['title']}\n\n")
            f.write(f"Description:\n{item['description']}\n\n")
            f.write(f"Table of Contents:\n{item['table_of_contents']}\n")

        return item

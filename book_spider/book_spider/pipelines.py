import os
import json


class BookPipeline:
    def process_item(self, item, spider):
        folder_name = 'scraped_data'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        filename = f"{folder_name}/{item['title'].replace(' ', '_')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dict(item), f, ensure_ascii=False, indent=4)

        return item
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapyZyyPipeline:
    def __init__(self):
        self.result_file = None

    def open_spider(self, spider):
        self.result_file = open('question-all.txt', 'a')
        print("Open result-file!")

    def process_item(self, item, spider):
        line = item['line']
        self.result_file.write(line)
        return item

    def close_spider(self, spider):
        self.result_file.close()
        print('Close result-file!')

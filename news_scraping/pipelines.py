# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from model.article import Article
from utils.database_util import insert_article
from utils.database_util import get_mysql_db_connection


class ArticlesPipeline:
    def __init__(self):
        self.cnx = None

    def __del__(self):
        if self.cnx is not None:
            self.cnx.close()

    def open_spider(self, spider):
        self.cnx = get_mysql_db_connection()

    def close_spider(self, spider):
        self.cnx.close()

    def process_item(self, item, spider):
        a = Article(item=item)
        insert_article(self.cnx, spider.website, a)
        return item

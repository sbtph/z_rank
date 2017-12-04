# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
<<<<<<< HEAD
from scrapy.exceptions import DropItem
import psycopg2
import psycopg2.extras

class DuplicatesPipeline(object):

    def __init__(self):
        self.urls_seen = set()
    def process_item(self, item, spider):
        if item['url'] in self.urls_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.urls_seen.add(item['url'])
            return item


class ZRankPipeline(object):

    def open_spider(self, spider):
        self.conn = psycopg2.connect(database="smzdm", user="postgres", \
        password="syiloveu559", host="localhost", port="5432")

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        try:
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            self.cur.execute("insert into zrank(title,price,mall,fav_count,comments_count,posted_at,vote_percent,url) \
            values (%(title)s,%(price)s,%(mall)s,%(fav_count)s,%(comments_count)s,\
            %(posted_at)s,%(vote_percent)s,%(url)s) ON CONFLICT(url) do update set fav_count=EXCLUDED.fav_count,\
            comments_count=EXCLUDED.comments_count,vote_percent=EXCLUDED.vote_percent;",dict(item))

        except Exception as e:
            print ('insert record into table failed')
            print (e)

        else:
            self.conn.commit()

=======


class ZRankPipeline(object):
    def process_item(self, item, spider):
>>>>>>> 3221a3ff8cc7dcf59e1cc2cead164c73c331e181
        return item

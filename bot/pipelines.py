# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import psycopg2
import psycopg2.extras

class DuplicatesPipeline(object):  # 查重

    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        if spider.name == "smzdm":
            if item['url'] in self.urls_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.urls_seen.add(item['url'])
                return item
        else:
            pass


class ZRankPipeline(object):

    def open_spider(self, spider):

        try:
            self.conn = psycopg2.connect(database="zrank", user="ban11111", \
                                         password="syiloveu559")#, host="localhost", port="5432")
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except Exception as e:
            print('Connect to db failed!')
            print(e)

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        if spider.name == "smzdm":
            try:
                self.cur.execute("insert into zrank(title,price,mall,fav_count,comments_count,posted_at,vote_percent,url,outdated) \
                values (%(title)s,%(price)s,%(mall)s,%(fav_count)s,%(comments_count)s,\
                %(posted_at)s,%(vote_percent)s,%(url)s, FALSE) ON CONFLICT(url) do update set fav_count=EXCLUDED.fav_count,\
                comments_count=EXCLUDED.comments_count,vote_percent=EXCLUDED.vote_percent;", item)
            except Exception as e:
                print('insert record into table failed')
                print(e)
            else:
                self.conn.commit()
            return item
        else:
            return item


'''class UpdatePipeline(object):
    def open_spider(self, spider):
        try:
            self.conn = psycopg2.connect(database="smzdm", user="postgres", \
                                         password="syiloveu559", host="localhost", port="5432")
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except Exception as e:
            print('Connect to db failed!')
            print(e)

    def close_spider(self, spider):

        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        if spider.name == "update2":
            try:
                print('**********************')
                print(item)
                self.cur.execute("update zrank set fav_count = %s,\
                            comments_count = %s, vote_percent = %s \
                            where url = %s ;", [item[fav_count],item[comments_count],item[vote_percent],item[url]])
            except Exception as e:
                print('insert record into table failed')
                print(e)
            else:
                self.conn.commit()
            return item
        else:
            pass'''

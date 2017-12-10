# -*- coding: utf-8 -*-
import scrapy
from z_rank.items import UpdateItem
import psycopg2
import psycopg2.extras

class UpdateSpider(scrapy.Spider):
    name = 'update'
    allowed_domains = ['www.smzdm.com']
    start_urls = []

    conn = psycopg2.connect(database="smzdm", user="postgres", \
                            password="syiloveu559", host="localhost", port="5432")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("select url from zrank where outdated = FALSE;")
    old_data = [j for i in cur.fetchall() for j in i] # 将 二维数组 转化为 一维数组 ！
    start_urls = old_data
    cur.close()
    conn.close()

    def parse(self, response):
        try:
            self.conn = psycopg2.connect(database="smzdm", user="postgres", \
                                         password="syiloveu559", host="localhost", port="5432")
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except Exception as e:
            print('Connect to db failed!')
            print(e)
        item = UpdateItem()
        zhi = int(response.css('#rating_worthy_num::text').extract_first())
        buzhi = int(response.css('#rating_unworthy_num::text').extract_first())
        item['vote_percent'] = int(zhi/(zhi+buzhi)*100) if zhi+buzhi != 0 else -1
        item['fav_count'] = int(response.css('.icon-collect + em::text').extract_first())
        item['comments_count'] = int(response.css('.commentNum::text').extract_first())
        item['url'] = response.url
        try:
            self.cur.execute("update zrank set fav_count = %(fav_count)s,\
                        comments_count = %(comments_count)s, vote_percent = %(vote_percent)s \
                        where url = %(url)s ;", item)
        except Exception as e:
            print('insert record into table failed')
            print(e)
        else:
            self.conn.commit()
        self.cur.close()
        self.conn.close()
        yield item

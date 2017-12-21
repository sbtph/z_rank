# -*- coding: utf-8 -*-
import scrapy
from bot.items import UpdateItem
from bot.connectdb import connectdb
import psycopg2.extras

class UpdateSpider(scrapy.Spider):
    name = 'update'
    allowed_domains = ['www.smzdm.com']
    start_urls = []

    conn = connectdb()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("select url from spider where outdated = FALSE or classification = NULL;")
    old_data = [j for i in cur.fetchall() for j in i] # 将 二维数组 转化为 一维数组 ！
    start_urls = old_data
    cur.close()
    conn.close()

    def parse(self, response):
        try:
            self.conn = connectdb()
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except Exception as e:
            print('Connect to db failed!')
            print(e)
        item = UpdateItem()
        zhi = int(response.css('#rating_worthy_num::text').extract_first())
        buzhi = int(response.css('#rating_unworthy_num::text').extract_first())
        item['zhi_count'] = zhi
        item['vote_percent'] = int(zhi/(zhi+buzhi)*100) if zhi+buzhi != 0 else -1
        item['fav_count'] = int(response.css('.icon-collect + em::text').extract_first())
        item['comments_count'] = int(response.css('.commentNum::text').extract_first())
        item['classification'] = response.xpath(
            "//div[@class='crumbs']/div[position()=2]/a/span/text()").extract_first()
        item['url'] = response.url
        try:
            self.cur.execute("update spider set fav_count = %(fav_count)s,zhi_count = %(zhi_count)s,\
                        comments_count = %(comments_count)s, vote_percent = %(vote_percent)s, \
                        classification = %(classification)s where url = %(url)s ;", item)
        except Exception as e:
            print('update record failed')
            print(e)
        else:
            self.conn.commit()
        self.cur.close()
        self.conn.close()
        yield item


class update_class(scrapy.Spider):
    name = 'class'
    allowed_domains = ['www.smzdm.com']
    start_urls = []
    conn = connectdb()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("select url from spider;")
    old_data = [j for i in cur.fetchall() for j in i]  # 将 二维数组 转化为 一维数组 ！
    start_urls = old_data
    cur.close()
    conn.close()

    def parse(self, response):
        try:
            self.conn = connectdb()
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except Exception as e:
            print('Connect to db failed!')
            print(e)
        self.item = {}
        self.item['classification'] = response.xpath("//div[@class='crumbs']/div[position()=2]/a/span/text()").extract_first()
        self.item['url'] = response.url
        print (self.item)
        try:
            self.cur.execute("update spider set classification = %(classification)s where url = %(url)s ;", self.item)
        except Exception as e:
            print('update record failed')
            print(e)
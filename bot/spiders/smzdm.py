# -*- coding: utf-8 -*-
import scrapy
from bot.items import ZRankItem
import datetime

class SmzdmSpider(scrapy.Spider):
    name = 'smzdm'
    allowed_domains = ['www.smzdm.com']
    start_urls = ['https://www.smzdm.com/jingxuan/']
    for i in range(2, 6):
        start_urls.append('https://www.smzdm.com/jingxuan/p' + str(i))

    #def __init__(self):
        #self.dateflag = False
        #self.parseflag = False
    def parse(self,response):
        #items = []
        list = response.css('#feed-main-list .feed-row-wide')
        item = ZRankItem()
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d')
        year = now.strftime('%Y-')
        for box in list:

            posted_text = box.css('.feed-block-extras::text').extract_first().rstrip()
            item['posted_at'] = year + posted_text if '-' in posted_text else date + ' ' + posted_text
            #if (now - datetime.datetime.strptime(item['posted_at'],'%Y-%m-%d %H:%M')).days > 0:
            #    self.dateflag = True
            #    break
            #title_texts = box.css('.feed-block-title::text')
            item['title'] = box.css('.feed-block-title a::text').extract_first()
            #print title_texts.css(' a::text').extract()
            item['price'] = box.css('.z-highlight::text').extract_first()
            zhi = int(box.css('.z-icon-zhi + span::text').extract_first())
            buzhi = int(box.css('.z-icon-buzhi + span::text').extract_first())
            item['zhi_count'] = zhi
            item['vote_percent'] = int(zhi/(zhi+buzhi)*100) if zhi+buzhi != 0 else -1
            item['fav_count'] = int(box.css('.z-icon-star-empty + span::text').extract_first())
            item['comments_count'] = int(box.css('.z-group-data::text').extract()[3])
            item['mall'] = box.css('.feed-block-extras a::text').extract_first().strip()
            item['url'] = box.css('.feed-block-title a::attr(href)').extract_first()
            item['img'] = "https://images.weserv.nl/?url=" + box.css('img::attr(src)').extract_first().replace("https://","")
            #yield scrapy.Request(item['url'], meta={'key': item}, callback=self.parse_class)
            yield item

        #print (item)
        #print('------------------------------------------------------')
        #print(response.url)

    def parse_class(self, response):
        item = response.meta['key']
        item['classification'] = response.xpath("//div[@class='crumbs']/div[position()=2]/a/span/text()").extract_first()
        #print ('--------------------------------------',item['classification'])
        yield item




    '''if self.parseflag == False:
            self.parseflag = True      # 利用flag设置循环仅运行一次。
            for i in range(2,6):       # 然而可以直接把网址写在 start_urls 里。
                page = 'https://www.smzdm.com/jingxuan/p' + str(i)
                yield scrapy.Request(page, callback=self.parse)'''

# -*- coding: utf-8 -*-
import scrapy
from z_rank.items import ZRankItem

class SmzdmSpider(scrapy.Spider):
    name = 'smzdm'
    allowed_domains = ['www.smzdm.com']
    start_urls = ['https://www.smzdm.com/jingxuan/']

    def parse(self, response):
        #items = []
        list = response.css('#feed-main-list .feed-row-wide')
        item = ZRankItem()
        for box in list:
            
            #title_texts = box.css('.feed-block-title::text')
            item['title'] = box.css('.feed-block-title a::text').extract_first()
            #print title_texts.css(' a::text').extract()
            item['price'] = box.css('.z-highlight::text').extract_first()
            zhi = int(box.css('.z-icon-zhi + span::text').extract_first())
            buzhi = int(box.css('.z-icon-buzhi + span::text').extract_first())
            item['vote_percent'] = int(zhi/(zhi+buzhi)*100) if zhi+buzhi != 0 else -1
            item['fav_count'] = int(box.css('.z-icon-star-empty + span::text').extract_first())
            item['comments_count'] = int(box.css('.z-group-data::text').extract()[3])
            item['posted_at'] = '2017-'+box.css('.feed-block-extras::text').extract_first().rstrip()
            item['mall'] = box.css('.feed-block-extras a::text').extract_first().strip()
            item['url'] = box.css('.feed-block-title a::attr(href)').extract_first()

            #items.append(item)
            yield item
        #print (item)
        for i in range(2,5):
            page = 'https://www.smzdm.com/jingxuan/' + 'p' + str(i) + '/'
            yield scrapy.Request(page, callback=self.parse)
            

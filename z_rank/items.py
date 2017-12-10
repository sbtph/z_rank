# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item as I
from scrapy import Field as F


class ZRankItem(I):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = F()
    price = F()
    mall = F()
    posted_at = F()
    fav_count = F()
    comments_count = F()
    vote_percent = F()
    url = F()

class UpdateItem(I):
    fav_count =  F()
    vote_percent = F()
    comments_count = F()
    url = F()
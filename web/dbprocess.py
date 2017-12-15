# coding: utf-8

from .models import Spider

def db_all_order_by(column):
    return list(Spider.objects.values().order_by('-' + column))

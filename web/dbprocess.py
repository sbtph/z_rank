# coding: utf-8

from .models import Spider

def db_all_order_by(column,colum2,fav=0,com=0,zhi=0,percent=0, **cf):
    #print(cf)
    if cf:
        data = Spider.objects.values().filter(fav_count__gte=fav). \
            filter(comments_count__gte=com).filter(zhi_count__gte=zhi). \
            filter(vote_percent__gte=percent).filter(classification__in=cf['ctxt']).exclude(outdated=True).\
            exclude(classification__isnull=True).order_by('-'+column, '-'+colum2)
    else:
        data = Spider.objects.values().filter(fav_count__gte=fav). \
            filter(comments_count__gte=com).filter(zhi_count__gte=zhi). \
            filter(vote_percent__gte=percent).exclude(outdated=True).exclude \
            (classification__isnull=True).order_by('-'+column, '-'+colum2)
    return list(data)

def db_class():
    return list(Spider.objects.all().values('classification').exclude(classification=None).\
                exclude(classification__contains="个人主页").exclude(outdated=True).distinct())
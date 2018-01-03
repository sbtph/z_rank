# coding: utf-8
from wechatpy import create_reply


def events_reply(msg):
    reply = None

    try:
        if msg.event == 'subscribe':
            reply = Subscribe(msg)
    except Exception as e:
        print('error:', e)
        reply = None
    return reply


def Subscribe(msg):
    reply = create_reply('欢迎关注zebreay的公众号，回复“排行”可以查看当前排行；回复“分类”可以查看全部分类；', msg)
    return reply

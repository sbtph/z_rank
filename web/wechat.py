# coding: utf-8
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from . import dbprocess as DB
from .wechat_events import events_reply

WECHAT_TOKEN = 'zebreayisban11111'
AES_Key = 'I8xlF0uNubVBfo8vazAQoh8YftYL6CMvvRUxetAa4Ju'
AppID = 'wx7945b4b4bcb70eae'

@csrf_exempt
def wechat(request):
    if request.method == 'GET':
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echo_str = request.GET.get('echostr', '')
        try:
            check_signature(WECHAT_TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            echo_str = 'error'
        response = HttpResponse(echo_str, content_type="text/plain")
        return response

    elif request.method == 'POST':
        from wechatpy.crypto import WeChatCrypto
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        #encrypt_type = request.GET.get('encrypt_type', '')
        msg_signature = request.GET.get('msg_signature', '')
        crypto = WeChatCrypto(WECHAT_TOKEN, AES_Key, AppID)
        decrypted_msg = crypto.decrypt_message(request.body, msg_signature, timestamp, nonce)
        msg = parse_message(decrypted_msg)
        if msg.type == 'text':
            if msg.content == "分类" or msg.content == "classification":
                classification = "目前有这些分类哦：" + ",".join(DB.db_class())
                reply = create_reply(classification, msg)
            else:
                reply = create_reply('回复“分类”可以查看分类哦', msg)
        elif msg.type == 'event':
            reply = events_reply(msg)
        else:
            reply = create_reply('这是啥，我读书少，看不懂哦……', msg)
        encrypted_xml = crypto.encrypt_message(reply.render(), nonce, timestamp)
        return HttpResponse(encrypted_xml, content_type="application/xml")

    else:
        return "nothing不可能运行到这里，哈哈~"
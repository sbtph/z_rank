# coding: utf-8
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException

WECHAT_TOKEN = 'zebreayisban11111'
AES_Key = 'I8xlF0uNubVBfo8vazAQoh8YftYL6CMvvRUxetAa4Ju'
AppID = 'wx7945b4b4bcb70eae'

@csrf_exempt
def wechat(request):
    signature = request.GET.get('signature', '')
    timestamp = request.GET.get('timestamp', '')
    nonce = request.GET.get('nonce', '')
    echo_str = request.GET.get('echostr', '')
    encrypt_type = request.GET.get('encrypt_type', '')
    msg_signature = request.GET.get('msg_signature', '')
    try:
        check_signature(WECHAT_TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        echo_str = 'error'
    if request.method == 'GET':
        response = HttpResponse(echo_str, content_type="text/plain")
        return response
    #elif request.method == 'POST':
    #POST 请求
    if encrypt_type == 'raw':
        msg = parse_message(request.body)
        response = HttpResponse(msg, content_type="application/xml")
        return response
    else:
        from wechatpy.crypto import WeChatCrypto

        crypto = WeChatCrypto(WECHAT_TOKEN, AES_Key, AppID)
        try:
            decrypted_xml = crypto.decrypt_message(
                request.body,
                msg_signature,
                timestamp,
                nonce
            )
        except (InvalidAppIdException, InvalidSignatureException):
            # 处理异常或忽略
            pass
        msg = parse_message(decrypted_xml)
        if msg.type == 'text':
            reply = create_reply('这是条文字消息', msg)
        else:
            reply = create_reply('这是其他类型消息', msg)
        encrypted_xml = crypto.encrypt_message(reply.render(), nonce, timestamp)
        return encrypted_xml

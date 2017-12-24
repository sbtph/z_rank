from django.shortcuts import render, HttpResponse
from . import dbprocess as DB
from django.conf import settings

# Create your views here.
def index(request):
    page = 24 # 每页显示的数量
    context = {}
    key_value = []
    a = 1
    for i in DB.db_class():
        key_value.append(['cf-' + str(a),i['classification']])
        a += 1
    context['classification'] = key_value

    if request.method == 'POST':
        post = request.POST
        if 'txt' in post.keys():

            if post['txt'] == '全部':
                list = DB.db_all_order_by('vote_percent', 'zhi_count')
                settings.Static_List = list
                context['list'] = list[0:page]
                context['scroll_times'] = '1'
                return render(request, 'list_container.html', context)

            elif post['txt'] == 'bottom':
                scroll = int(post['scroll'])
                list = settings.Static_List[scroll*page:scroll*page+page]
                context['list'] = list
                context['scroll_times'] = str(scroll+1)
                context['finish'] = True if scroll*page+page >= len(settings.Static_List) else False
                if context['finish']==True:
                    settings.Static_List = ['finish']
                return render(request, 'list_container.html', context)
        else:
            ctxt = []
            for i in range(0, len(post)):
                if 'ctxt['+str(i)+']' in post.keys():
                    ctxt.append(post['ctxt['+str(i)+']'])
                else:
                    break
            if ctxt:
                list = DB.db_all_order_by('vote_percent','zhi_count',fav=0,com=0,zhi=0,percent=0,scroll='n',ctxt=ctxt)
                settings.Static_List = list
            else:
                list = DB.db_all_order_by('vote_percent', 'zhi_count')
                settings.Static_List = list

            context['list'] = list[0:page]
            context['scroll_times'] = '1'
            return render(request, 'list_container.html', context)

    elif request.method == 'GET':
        list = DB.db_all_order_by('vote_percent', 'zhi_count')
        settings.Static_List = list
        context['list'] = list[0:page]
        return render(request, 'index.html', context)

    else:
        return HttpResponse("服务器错误！程序猿拼命修复中，请稍后尝试访问，谢谢~~~~")

def bs(request):
    return render(request,'index_bootstrap.html')

def user(request):
    context = {}
    test = DB.db_all_order_by('zhi_count')
    context['c1'] = test
    context['c2'] = [12,13,14]
    return render(request, 'user.html', context)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def user_login(request):
    if request.method == 'GET':
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        # TODO:显示登陆页面，blablabla
    elif request.method == 'POST':
        # TODO: 用户登录操作，blablabla
        #  重定向到来源的url
        return HttpResponseRedirect(request.session['login_from'])
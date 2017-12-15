from django.shortcuts import render
from django.urls import reverse
from . import dbprocess as DB

# Create your views here.
def index(request):
    context = {}
    context['c1'] = 'Hello World!'
    all_data = DB.db_all_order_by('vote_percent')
    context['c2'] = all_data
    return render(request, 'index.html', context)


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
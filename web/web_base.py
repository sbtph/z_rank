# coding: utf-8
from django.shortcuts import render

def base(request):
    context = {}
    context['c1'] = 'Hello World!'
    return render(request, 'base.html', context)
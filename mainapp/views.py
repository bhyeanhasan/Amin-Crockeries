from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .models import DP


# Create your views here.

def dp(request):
    dps = DP.objects.all
    return render(request, 'index.html', {'dp': dps})


def articles(request):
    keyword = request.GET.get("key")
    if len(keyword)>0:
        articles = DP.objects.filter(name__contains=keyword)
        if len(articles)>0:
            return render(request, "articles.html", {"articles": articles})
        else:
            ob = DP()
            ob.name = 'not found'
            ob.img = 'asa.jpg'
            ob.res = 00
            articles = [ob]
            return render(request, "articles.html", {"articles": articles})
    else:
        ob = DP()
        ob.name = 'No Product Found'
        ob.img = 'asa.jpeg'
        ob.res = 000
        articles = [ob]
        return render(request, "articles.html", {"articles": articles})


def pitol(request):
    articles = DP.objects.filter(tag__contains='pitol')
    return render(request, "articles.html", {"articles": articles})


def dinner(request):
    articles = DP.objects.filter(tag__contains='dinner')
    return render(request, "articles.html", {"articles": articles})


def frypan(request):
    articles = DP.objects.filter(tag__contains='frypan')
    return render(request, "articles.html", {"articles": articles})


def steel(request):
    articles = DP.objects.filter(tag__contains='steel')
    return render(request, "articles.html", {"articles": articles})


def rice(request):
    articles = DP.objects.filter(tag__contains='rice')
    return render(request, "articles.html", {"articles": articles})


def pressure(request):
    articles = DP.objects.filter(tag__contains='pressure')
    return render(request, "articles.html", {"articles": articles})


def blender(request):
    articles = DP.objects.filter(tag__contains='blender')
    return render(request, "articles.html", {"articles": articles})


def glass(request):
    articles = DP.objects.filter(tag__contains='glass')
    return render(request, "articles.html", {"articles": articles})


def plastic(request):
    articles = DP.objects.filter(tag__contains='plastic')
    return render(request, "articles.html", {"articles": articles})


def alu(request):
    articles = DP.objects.filter(tag__contains='alu')
    return render(request, "articles.html", {"articles": articles})


def other(request):
    articles = DP.objects.filter(tag__contains='other')
    return render(request, "articles.html", {"articles": articles})

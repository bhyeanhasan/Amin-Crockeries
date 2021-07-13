from django.contrib import admin
from django.urls import path,include
from mainapp import views

urlpatterns = [
    path('', views.product_list, name='home'),
    path('details/<id>/', views.details, name='details'),
    path('addtocard/<id>/', views.addToCard, name='addToCard'),
    path('newTEm/', views.newTem, name='newTem'),
    path('articles/', views.articles, name='articles'),
    path('pitol/', views.pitol, name='pitol'),
    path('dinner/', views.dinner, name='dinner'),
    path('steel/', views.steel, name='steel'),
    path('frypan/', views.frypan, name='frypan'),
    path('rice/', views.rice, name='rice'),
    path('pressure/', views.pressure, name='pressure'),
    path('blender/', views.blender, name='blender'),
    path('glass/', views.glass, name='glass'),
    path('plastic/', views.plastic, name='plastic'),
    path('alu/', views.alu, name='alu'),
    path('other/', views.other, name='other'),

]

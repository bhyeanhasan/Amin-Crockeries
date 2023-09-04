from django.contrib import admin
from django.urls import path, include
from mainapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.product_list, name='home'),
                  path('details/<id>/', views.details, name='details'),
                  path('category/<tag>/', views.category, name='category'),
                  path('addtocard/<id>/', views.addToCard, name='addToCard'),
                  path('deleteallcart/<id>/', views.deleteallcart, name='deleteallcart'),
                  path('deletefromcart/<id>/', views.deletefromcart, name='deletefromcart'),
                  path('addtowish/<id>/', views.addToWish, name='addToWish'),
                  path('showWish/', views.showWish, name='showWish'),
                  path('search_result/', views.search_result, name='search_result'),
                  path('about/', views.about, name='about'),
                  path('cart/', views.cart, name='cart'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

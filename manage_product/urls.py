from django.contrib import admin
from django.urls import path, include
from manage_product import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.product_list, name='home'),
                  path('details/<id>/', views.details, name='details'),
                  path('category/<id>/', views.category, name='category'),
                  path('searchresult/', views.search_result, name='search_result'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

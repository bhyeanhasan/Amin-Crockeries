from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import Group

admin.site.site_header = "Amin Crockeries"
admin.site.site_title = "Amin Crockeries"
admin.site.index_title = "Welcome to Amin Crockeries"

urlpatterns = [
                  path('', include('manage_product.urls')),
                  path('manage_user/', include('manage_user.urls')),
                  path('manage_order/', include('manage_order.urls')),
                  path('manage_api/', include('manage_api.urls')),
                  path('admin/', admin.site.urls),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

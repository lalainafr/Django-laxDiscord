
from django.contrib import admin
from django.urls import path, include

# necéssaire pour les fichiers uploaded
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    
    # on inclut l'url de l'api
    path('api/', include('base.api.urls')),
]

# set the  url  and get the file from MEDIA_ROOT 
# connect MEDIA_ROOT to MEDIA_URL
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


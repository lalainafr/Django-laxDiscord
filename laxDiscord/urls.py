
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    
    # on inclut l'url de l'api
    path('api/', include('base.api.urls')),

]

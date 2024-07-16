from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('customizer.urls')), 
    path('user/', include('custom_profile.urls')),
]

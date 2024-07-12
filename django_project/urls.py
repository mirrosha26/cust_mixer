from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('customizer.urls')), 
    path('user/', include('custom_profile.urls')), 
]
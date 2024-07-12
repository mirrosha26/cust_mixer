from django.contrib import admin
from django.urls import path
from .views import SigninView, LogoutView, theme_view

urlpatterns = [
    path('signin/', SigninView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('style.css', theme_view, name='style'),
]
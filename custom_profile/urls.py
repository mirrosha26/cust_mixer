from django.contrib import admin
from django.urls import path
from .views import SigninView, LogoutView, theme_view, create_user, update_user_status

urlpatterns = [
    path('signin/', SigninView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create-user/', create_user, name='create_user'),
    path('update-user-status/', update_user_status, name='update_user_status'),
    path('style.css', theme_view, name='style'),
]
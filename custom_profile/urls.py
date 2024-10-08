from django.contrib import admin
from django.urls import path
from .views import SigninView, LogoutView, theme_view, create_user, update_user_status, theme_js_view
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    custom_password_reset_complete,
    get_html_content
)

urlpatterns = [
    path('signin/', SigninView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create-user/', create_user, name='create_user'),
    path('update-user-status/', update_user_status, name='update_user_status'),
    path('style.css', theme_view, name='style'),
    path('script.js', theme_js_view, name='js'),
    path('reset_password/', CustomPasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', custom_password_reset_complete, name='password_reset_complete'),
    path('get_html_content/', get_html_content, name='get_html_content')
]
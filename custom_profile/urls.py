from django.contrib import admin
from django.urls import path
from .views import SigninView, LogoutView, theme_view, create_user, update_user_status
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView
)

urlpatterns = [
    path('signin/', SigninView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create-user/', create_user, name='create_user'),
    path('update-user-status/', update_user_status, name='update_user_status'),
    path('style.css', theme_view, name='style'),
    path('reset_password/', CustomPasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
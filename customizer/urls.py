from django.urls import path
from . import views


urlpatterns = [
    path('main', views.MainCustomizerView.as_view(), name='custom_main'),
    path('lesson', views.LessonCustomizerView.as_view(), name='custom_lesson'), 
    path('card', views.CardCustomizerView.as_view(), name='custom_card'), 
    path('', views.LoginCustomizerView.as_view(), name='custom_login'), 
    path('navigation', views.NavigationCustomizerView.as_view(), name='custom_navigation'), 
    path('baners', views.BanerCustomizerView.as_view(), name='baner'), 
    path('script', views.ScriptCustomizerView.as_view(), name='custom_script'), 

    path('reset-theme-settings/', views.reset_theme_settings, name='reset_theme_settings'),

]
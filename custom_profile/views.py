from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import JsonResponse
from customizer.models import ThemeSettings
from django.http import HttpResponseForbidden
from custom_profile.models import User
from customizer.models import ThemeSettings

class SigninView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('custom_main')
        return render(request, 'custom_profile/index.html', {})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'custom_profile/index.html', {'error': 'Имя пользователя и пароль обязательны для заполнения'})

        User = get_user_model()
        if not User.objects.filter(username=username).exists():
            return render(request, 'custom_profile/index.html', {'error': 'Пользователь с таким именем не найден'})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('custom_main')
        else:
            return render(request, 'custom_profile/index.html', {'error': 'Неверный пароль. Попробуйте снова.'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('signin')


def theme_view(request):
    uuid = request.GET.get('uuid')
    domain = request.GET.get('d')
    if not uuid or not domain:
        return HttpResponseForbidden("Access Denied")
    user = get_object_or_404(User, uuid=uuid)
    if user.domain != domain:
        return HttpResponseForbidden("Access Denied")
    theme_settings = get_object_or_404(ThemeSettings, user=user)
    return render(request, 'style/return.css', {'theme_settings': theme_settings})
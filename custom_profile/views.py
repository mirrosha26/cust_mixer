from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import JsonResponse
from customizer.models import ThemeSettings
from django.http import HttpResponseForbidden
from custom_profile.models import User
from customizer.models import ThemeSettings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password

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
    return render(request, 'style/return.css', {'theme_settings': theme_settings}, content_type='text/css')


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        order_id = request.POST.get('order_id')
        
        if not email or not password or not order_id:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'User with this email already exists'}, status=400)
        
        user = User.objects.create(
            username=email,
            email=email,
            password=make_password(password),
            order_id=order_id
        )
        
        return JsonResponse({'message': 'User created successfully', 'uuid': user.uuid}, status=201)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def update_user_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        is_connected = request.POST.get('is_connected')

        if not order_id or is_connected is None:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            is_connected = bool(int(is_connected))
        except ValueError:
            return JsonResponse({'error': 'Invalid value for is_connected'}, status=400)

        try:
            user = User.objects.get(order_id=order_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User with this order_id does not exist'}, status=404)

        user.is_connected = is_connected
        user.save()

        return JsonResponse({'message': 'User status updated successfully'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
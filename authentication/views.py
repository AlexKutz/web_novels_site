import json
from io import BytesIO
from PIL import Image
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlencode
from .forms import CustomUserCreationForm, EmailChangeForm


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'authentication/profile.html')
    else:
        login_url = reverse('login')+'?'+urlencode({'next': request.path})
        return redirect(login_url)


def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            login_url = reverse('login') + '?' + urlencode({'next': request.path})
            return redirect(login_url)
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/registration.html', {'form': form})


@login_required(redirect_field_name='login')
def email_change(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = EmailChangeForm(request.user, data)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'message': 'Электронная почта изменена',
                'new_email': data.get('new_email'),
            }, safe=False)
        else:
            errors = form.errors.as_data()
            print(errors)
            return JsonResponse({
                'message': form.errors,
            }, safe=False, status=400)


@login_required(redirect_field_name='login')
def account_image_change(request):
    if request.method == 'POST':
        if request.FILES.get('image'):
            file = request.FILES.get('image')
            pil_image = Image.open(file)
            # pil_image = pil_image.resize((200, 200), Image.LANCZOS)
            io = BytesIO()
            pil_image.save(io, 'PNG', quality=100)
            image = File(io, name='%s.png' % request.user.username)
            request.user.image.delete()
            request.user.image = image
            request.user.save()
            return JsonResponse({
                'message': 'Фото профиля изменено',
            }, safe=False, status=200)
        return JsonResponse({
            'message': 'Не передано изображение',
        }, safe=False, status=400)
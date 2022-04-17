import datetime
import json
from io import BytesIO
from PIL import Image
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.files import File
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlencode, urlsafe_base64_encode, urlsafe_base64_decode
from .forms import CustomUserCreationForm, EmailChangeForm
from .models import User
from .utils import mul_of_num
import binascii, os
from novel.models import UserBookShelfBook

def profile(request):
    if request.user.is_authenticated:
        bookShelf = UserBookShelfBook.objects.filter(user = request.user)
        novels = []
        for novel in bookShelf:
            novels.append(novel.novel)
        ctx = {
            'novel': novels
        }
        return render(request, 'authentication/profile.html', ctx)
    else:
        login_url = reverse('login') + '?' + urlencode({'next': request.path})
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
        change_datetime = datetime.datetime.fromisoformat(request.session.get('email_change_datetime'))
        if change_datetime:
            current_datetime = datetime.datetime.now()
            print('current', current_datetime, 'change:', change_datetime)
            next_change = 60 - (current_datetime - change_datetime).total_seconds() / 60.0
            if next_change > 0:
                return JsonResponse({
                    'message': f'Следущий раз вы можете изменить почту через {int(next_change)} {mul_of_num(int(next_change))}'
                }, status=400)
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
            new_image_name = binascii.b2a_hex(os.urandom(8))
            file = request.FILES.get('image')
            pil_image = Image.open(file)
            pil_image = pil_image.resize((200, 200), Image.LANCZOS)
            io = BytesIO()
            pil_image.save(io, 'PNG', quality=100)
            image = File(io, name='%s.png' % new_image_name)
            request.user.image.delete()
            request.user.image = image
            request.user.save()
            return JsonResponse({
                'message': 'Фото профиля изменено',
            }, status=200)
        return JsonResponse({
            'message': 'Не передано изображение',
        }, safe=False)


UserModel = get_user_model()


def send_activation_email(request):
    site = get_current_site(request)
    mail_subject = 'Активация аккауна Novel.com'
    message = render_to_string('authentication/active_email.html', {
        'user': request.user,
        'domain': site.domain,
        'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
        'token': default_token_generator.make_token(request.user)
    })
    to_email = request.user.email
    if to_email:
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        current_datetime = datetime.datetime.now()
        request.session['email_change_datetime'] = current_datetime.isoformat()
        return JsonResponse({
            'message': 'Письмо отправлено. Пожалуйста проверить свою почту.'
        }, status=200)
    else:
        return JsonResponse({'message': 'Пользователь не установил электронную почту'}, status=400)


def activate(request, uidb64, token):
    pass
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active_email = True
        user.save()
        return HttpResponse('Электронная почта потвержена успешно')
    else:
        return HttpResponse('Неправильная ссылка')

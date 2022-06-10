from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import UserLoginForm

urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('email_change', views.email_change, name='email_change'),
    path('login', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=UserLoginForm), name='login'),
    path('registration', views.registration, name='registration'),
    path('image', views.account_image_change, name='image'),
    path('send_activation_email', views.send_activation_email, name='email'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]

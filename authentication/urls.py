from django.urls import path

from . import views

urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('email_change', views.email_change, name='email_change'),
    path('registration', views.registration, name='registration'),
    path('image', views.account_image_change, name='image'),
    path('send_activation_email', views.send_activation_email, name='email'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate')
]

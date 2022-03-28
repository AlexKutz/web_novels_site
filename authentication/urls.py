from django.urls import path

from . import views

urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('email_change', views.email_change, name='email_change'),
    path('registration', views.registration, name='registration'),
]

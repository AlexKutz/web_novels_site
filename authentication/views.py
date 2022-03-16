from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils.http import urlencode


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'authentication/profile.html')
    else:
        login_url = reverse('login')+'?'+urlencode({'next': request.path})
        return redirect(login_url)

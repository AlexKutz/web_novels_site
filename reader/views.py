from django.http import HttpResponse
from django.shortcuts import render


def read():
    return HttpResponse('word')
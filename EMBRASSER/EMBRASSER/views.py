import json

from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

from config.State import State


def index(request):
    return render(request, 'index.html')
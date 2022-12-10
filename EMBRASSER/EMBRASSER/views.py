from ocr_module.first_ocr import *

from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

import json

def index(request):
    return render(request, 'index.html')

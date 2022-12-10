from django.core.files.storage import FileSystemStorage
from PIL import Image
from ocr_module.first_ocr import *
import os
import json

from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse

from config.State import State

from EMBRASSER.models import Members
import requests
import uuid
import time
import json

def index(request):
    return render(request, 'index.html')

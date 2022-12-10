from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('coocr_upload', views.coocr_upload),
    path('join_member', views.joinmember),
]
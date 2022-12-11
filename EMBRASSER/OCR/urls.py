from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('coocr_first', views.coocr_first),
    path('coocr_second', views.coocr_second),
    path('coocr_third', views.coocr_third),
    path('join_member', views.join_member),
]
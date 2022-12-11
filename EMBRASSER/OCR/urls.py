from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('coocr_upload', views.coocr_upload),
    path('joinmember', views.joinmember),
    path('all_statistics', views.all_statistics),
    path('grade_statistics', views.grade_statistics),
    path('sex_statistics', views.sex_statistics),
]
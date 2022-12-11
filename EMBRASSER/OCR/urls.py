from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('coocr_upload', views.coocr_upload),
    path('joinmember', views.joinmember),
    path('modify_customer', views.modify_customer),
    path('modify_confirm', views.modify_confirm),
    path('list', views.member_list),
]
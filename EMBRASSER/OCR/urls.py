from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('coocr_upload', views.coocr_upload),
    path('joinmember', views.joinmember),
    path('all_statistics', views.all_statistics),
    path('grade_statistics', views.grade_statistics),
    path('sex_statistics', views.sex_statistics),
    path('modify_customer', views.modify_customer),
    path('modify_confirm', views.modify_confirm),
    path('delete_customer',views.delete_customer),
    path('list', views.member_list),
    path('search', views.member_search),
]
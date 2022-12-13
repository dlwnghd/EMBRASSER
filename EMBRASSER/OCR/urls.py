from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('coocr_first', views.coocr_first),
    path('coocr_second', views.coocr_second),
    path('coocr_third', views.coocr_third),
    path('join_member', views.join_member),
    path('event_first', views.event_first),
    path('event_second', views.event_second),
    path('event_update', views.event_update),
    path('all_statistics', views.all_statistics),
    path('grade_statistics', views.grade_statistics),
    path('sex_statistics', views.sex_statistics),
    path('modify_customer', views.modify_customer),
    path('modify_confirm', views.modify_confirm),
    path('delete_customer',views.delete_customer),
    path('list', views.member_list),
    path('search', views.member_search),
    path('matching', views.member_matching),
]
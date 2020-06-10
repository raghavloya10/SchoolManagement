from django.contrib import admin
from django.urls import path,include
from . import views

app_name = "admins"

urlpatterns = [
    path('signup/',views.signup_view,name='home'),
    path('standard_list',views.standard_list_view,name='standard_list'),
    path('student_list/<slug:slug>/',views.student_list_view,name='student_list'),
    path('student_update/<slug:slug>/',views.student_update_view,name='student_update'),
    path('refresh_standard/<slug:slug>/',views.refresh_standard_view,name='refresh_standard'),
    path('subject_list/<slug:slug>/',views.subject_list_view,name='subject_list')
]

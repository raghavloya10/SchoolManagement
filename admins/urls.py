from django.contrib import admin
from django.urls import path,include
from . import views
from calendars import views as cal_views

app_name = "admins"

urlpatterns = [
    path('signup/',views.signup_view,name='home'),
    path('standard_list',views.standard_list_view,name='standard_list'),
    path('student_list/<slug:slug>/',views.student_list_view,name='student_list'),
    path('all_student_list/',views.all_student_list,name='all_student_list'),
    path('all_teacher_list/',views.all_teacher_list,name='all_teacher_list'),
    path('student_update/<slug:slug>/',views.student_update_view,name='student_update'),
    path('teacher_update/<slug:slug>/',views.teacher_update_view,name='teacher_update'),
    path('refresh_standard/<slug:slug>/',views.refresh_standard_view,name='refresh_standard'),
    path('subject_list/<slug:slug>/',views.subject_list_view,name='subject_list'),
    path('subject_update/<slug:slug>/',views.subject_update_view,name='subject_update'),
    path('class_teacher_update/<slug:slug>/',views.class_teacher_update,name='class_teacher_update'),
    path('student_profile/<slug:slug>/',views.student_profile_view,name='student_profile'),
    path('teacher_profile/<slug:slug>/',views.teacher_profile_view,name='teacher_profile'),

    path('calendar/',cal_views.admin_calendar,name='calendar'),
    path('event/new/',cal_views.event,name='event_new'),
    path('event/edit/<slug:slug>/',cal_views.event, name="event_edit"),
    path('event/delete/<slug:slug>/',cal_views.event_delete, name="event_delete"),
    
]

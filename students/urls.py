from django.contrib import admin
from django.urls import path,include
from . import views
from calendars import views as cal_views

app_name = 'students'

urlpatterns = [
    path('home/',views.student_home_view,name='home'),
    path('profile/<slug:slug>/',views.student_profile_view,name='profile'),
    path('gradebook/',views.student_gradebook_view,name='gradebook'),
    path('grades/<slug:slug>',views.student_grades,name='grades'),
    path('profile_pic_update/',views.profile_pic_update_view,name='profile_pic_update'),

    path('calendar/',cal_views.student_calendar,name='calendar'),
    path('event/new/',cal_views.event,name='event_new'),
    path('event/edit/<slug:slug>/',cal_views.event, name="event_edit")
]

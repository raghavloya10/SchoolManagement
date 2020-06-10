from django.contrib import admin
from django.urls import path,include
from . import views
from uploads import views as upload_views

app_name = 'teachers'

urlpatterns = [
    path('home/',views.TeacherTemplateView.as_view(),name='home'),
    path('profile/<slug:slug>/',views.teacher_profile_view,name='profile'),
    # path('calendar/',calendars.views.CalendarView.as_view(),name='calendar'),
    path('update_result/<slug:slug>/',views.class_result_update,name='update_result'),
    path('upload/<slug:slug>/',upload_views.upload_view,name='upload'),
    path('upload/delete/<slug:slug>/',upload_views.delete_view,name='delete_upload'),

    # path('class_teacher_home/<int:pk>',views.class_teacher_view,name='class_teacher_home')
]

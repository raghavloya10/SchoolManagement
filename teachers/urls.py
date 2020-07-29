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
    path('class_teacher_home/',views.class_teacher_home,name="class_teacher_home"),
    path('profile_pic_update/',views.profile_pic_update_view,name='profile_pic_update'),

    path('class_teacher/student_grade/<slug:slug>/',views.student_grade_view,name="student_grade")
]

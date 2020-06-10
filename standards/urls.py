from django.contrib import admin
from django.urls import path,include
from . import views
from uploads import views as upload_views

app_name = 'standards'

urlpatterns = [
    path('class_teacher_home/',views.StandardTemplateView.as_view(),name='class_teacher_home'),
    # path('class_teacher_home/<int:pk>',views.class_teacher_view,name='class_teacher_home')
]

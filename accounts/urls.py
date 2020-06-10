from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('',views.login_view,name='login'),
    path('logout/',views.logout_view, name="logout")
]

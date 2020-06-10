from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView,ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import authenticate,logout,login

from students.models import Student
from teachers.models import Teacher
from accounts.models import User
from standards.models import Standard
from .forms import UserLoginForm

def login_view(request):
    if request.user.is_authenticated:
        if request.user.admin:
            return redirect('admins:home')
        if request.user.is_student:
            student = Student.objects.get(user=request.user)
            return redirect('students:home')
        elif request.user.is_teacher:
            teacher = Teacher.objects.get(user=request.user)
            return redirect('teachers:home')
        else:
            return HttpResponse('<h1>You are neither a teacher nor a student</h1>')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get('password')
            user = authenticate(email=email,password=password)
            login(request, user)
            if user is None:
                return HttpResponse('<h1>No fucking user found</h1>')
            if user.admin:
                return redirect('admins:home')
            if user.is_student:
                student = Student.objects.get(user=request.user)
                request.session['name'] = email
                request.session['password'] = password
                return redirect('students:home')
            elif user.is_teacher:
                teacher = Teacher.objects.get(user=request.user)
                request.session['name'] = email
                request.session['password'] = password
                return redirect('teachers:home')
            else:
                return redirect('admin')
            # else:
            #     form = UserLoginForm()
            #     return render(request, 'account/login.html', {'form':form, 'wrong':True})
        else:
            print(form.errors)

    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form':form})

@login_required
def logout_view(request):
    try:
        del request.session['name']
        del request.session['password']
    except KeyError:
        pass
    logout(request)
    return redirect('accounts:login')

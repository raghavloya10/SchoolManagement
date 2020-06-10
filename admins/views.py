from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.generic import (TemplateView,ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)

from students.models import Student
from results.models import Result, Examination
from teachers.models import Teacher
from subjects.models import Subject
from standards.models import Standard, ClassTeacher
from accounts.models import User
from uploads.models import Upload

from .forms import (UserSignupForm,
                    StudentExtraForm,
                    StudentUpdateForm,
                    RefreshStandardForm)

@login_required
def signup_view(request):
    if not request.user.admin:
        return HttpResponse('<h1>You are not authorised to view this page</h1>')

    if request.method == 'POST':
        form = UserSignupForm(request.POST, request.FILES)
        form2 = StudentExtraForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user.save()
            user = authenticate(email=email, password=password)
            role = request.POST.get('role')
            login(request,user)
            if role == 'Teacher':
                user = request.user
                user.is_teacher = True
                user.is_student = False
                user.save()
                teacher = Teacher(user=user)
                teacher.save()
                return redirect('teachers:home')
            else:
                if form2.is_valid():
                    user = request.user
                    user.is_student = True
                    user.save()
                    student = form2.save(user)
                    student.standards.add(student.current_standard)
                    student.save()
                    return redirect('students:home')

    else:
        form = UserSignupForm()
        form2 = StudentExtraForm()

    return render(request, 'admins/home.html', {'form': form, 'studentForm':form2})

@login_required
def standard_list_view(request):
    if not request.user.admin:
        return HttpResponse('<h1>Aukaat bhai aukaaaat</h1>')
    standards = Standard.objects.all()
    return render(request,'admins/standard_list.html',{'standards':standards})

@login_required
def student_list_view(request,slug):
    if not request.user.admin:
        return HttpResponse('<h1>Aukaat bhai aukaaaat</h1>')
    standard = Standard.objects.get(slug=slug)
    students = Student.objects.filter(current_standard=standard).order_by('roll_number')
    dict = {
        'students':students,
        'standard':standard
    }
    return render(request,'admins/student_list.html',context=dict)

@login_required
def subject_list_view(request,slug):
    if not request.user.admin:
        return HttpResponse('<h1>Aukaat bhai aukaaaat</h1>')
    standard = Standard.objects.get(slug=slug)
    subjects = Subject.objects.filter(standard=standard).order_by('name')
    dict = {
        'subjects':subjects,
        'standard':standard
    }
    return render(request,'admins/subject_list.html',dict)

@login_required
def student_update_view(request,slug):
    if not request.user.admin:
        return HttpResponse('<h1>Aukaat mein raho</h1>')
    student = Student.objects.get(slug=slug)
    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('admins:home')
    else:
        form = StudentUpdateForm(instance=student)
        context = {
            'student':student
        }
        return render(request,'admins/student_update.html',{'form':form})

@login_required
def refresh_standard_view(request,slug):
    standard = Standard.objects.get(slug=slug)
    if request.method == 'POST':
        form = RefreshStandardForm(request.POST)
        if form.is_valid():
            students = Student.objects.filter(current_standard=standard)
            for student in students:
                student.current_standard = None
                student.save()
            new = form.cleaned_data.get('students')
            for student in new:
                student.current_standard = standard
                student.standards.add(standard)
                student.save()
            return redirect('admins:student_list',slug=slug)

        else:
            return HttpResponse('<h1>fo</h1>')

    form = RefreshStandardForm(initial={'students':Student.objects.filter(current_standard=standard)})
    return render(request,'admins/refresh_standard.html',{'form':form,'standard':standard})

@login_required
def update_subject_teacher(request):
    if not request.user.admin:
        return HttpResponse('<h1>You are not authorised to view this page</h1>')
    standards = Standard.objects.all()
    subjects = {}
    for standard in standards:
        subjects[standard] = Subject.objects.get(standard=standard)
    return render(request,'admins/teacher_update')

@login_required
def update_class_teacher(request, standard_slug, teacher_slug):
    standard = Standard.objects.get(standard_slug)
    teacher = Teacher.objects.get(teacher_slug)
    class_teacher = ClassTeacher.objects.get(standard=standard)
    ex_teacher = class_teacher.teacher
    ex_teacher.is_class_teacher = False
    class_teacher.teacher = teacher
    teacher.is_class_teacher = True
    teacher.save()
    class_teacher.save()
    ex_teacher.save()
    return render(request,'admins:home')

@login_required
def class_teacher_view(request):
    pass

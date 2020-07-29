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

from .forms import (UserSignupForm, StudentExtraForm,
                    StudentUpdateForm, RefreshStandardForm,
                    SubjectUpdateForm, UserUpdateForm,
                    ClassTeacherUpdateForm, TeacherUpdateForm)

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
def subject_update_view(request,slug):
    if not request.user.admin:
        return HttpResponse('<h1>Aukaat bhai aukaaaat</h1>')
    subject = Subject.objects.get(slug=slug)
    if request.method == 'POST':
        form = SubjectUpdateForm(request.POST)
        if form.is_valid():
            subject.teacher = form.cleaned_data.get('teacher')
            subject.save()
            return redirect('admins:subject_list',slug=subject.standard.slug)
        else:
            return HttpResponse('<h1>fo</h1>')

    form = SubjectUpdateForm(initial={'teacher':subject.teacher})
    return render(request,'admins/subject_teacher_update.html',{'form':form,'subject':subject})

@login_required
def student_update_view(request,slug):
    if not request.user.admin:
        return HttpResponse('<h1>Aukaat mein raho</h1>')
    student = Student.objects.get(slug=slug)
    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, request.FILES, instance=student)
        form1 = UserUpdateForm(request.POST, request.FILES, instance=student.user)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            return redirect('admins:home')
    else:
        form = StudentUpdateForm(instance=student)
        form1 = UserUpdateForm(instance=student.user)
        return render(request,'admins/student_update.html',{'form':form,'userform':form1,'student':student})

@login_required
def teacher_update_view(request,slug):
    if not request.user.admin:
        return HttpResponse('<h1>Aukaat mein raho</h1>')
    teacher = Teacher.objects.get(slug=slug)
    if request.method == 'POST':
        form = TeacherUpdateForm(request.POST, request.FILES, instance=teacher)
        form1 = UserUpdateForm(request.POST, request.FILES, instance=teacher.user)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            return redirect('admins:standard_list')
    else:
        form = TeacherUpdateForm(instance=teacher)
        form1 = UserUpdateForm(instance=teacher.user)
        return render(request,'admins/teacher_update.html',{'form':form,'userform':form1,'teacher':teacher})

@login_required
def class_teacher_update(request,slug):
    if not request.user.admin:
        return HttpResponse('<h1>Aukaat mein raho</h1>')
    standard = Standard.objects.get(slug=slug)
    class_teacher = standard.class_teacher
    if request.method == 'POST':
        form = ClassTeacherUpdateForm(request.POST)
        if form.is_valid():
            class_teacher.teacher = form.cleaned_data.get('teacher')
            class_teacher.save()
            return redirect('admins:standard_list')
        else:
            return HttpResponse("Form not valid")
    form = ClassTeacherUpdateForm(initial={'teacher':class_teacher.teacher})
    return render(request,'admins/class_teacher_update.html',{'form':form,'class_teacher':class_teacher})

@login_required
def refresh_standard_view(request,slug):
    if not request.user.admin:
        return HttpResponse('<h1>Aukaat mein raho</h1>')
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
def all_student_list(request):
    if not request.user.admin:
        return HttpResponse('<h1>Aukaat mein raho</h1>')
    if request.method == 'POST':
        student = Student.objects.get(user__email=request.POST['stud'])
        return redirect('admins:student_profile',slug=student.slug)
    students = Student.objects.all()
    return render(request,'admins/all_student_list.html',{'students':students})

@login_required
def all_teacher_list(request):
    if not request.user.admin:
        return HttpResponse('<h1>Aukaat mein raho</h1>')
    if request.method == 'POST':
        teacher = Teacher.objects.get(user__email=request.POST['stud'])
        return redirect('admins:teacher_profile',slug=teacher.slug)
    teachers = Teacher.objects.all()
    return render(request,'admins/all_teacher_list.html',{'teachers':teachers})

@login_required
def student_profile_view(request,slug):
    student = Student.objects.get(slug=slug)
    return render(request,'admins/student_profile.html',{'student':student})

@login_required
def teacher_profile_view(request,slug):
    teacher = Teacher.objects.get(slug=slug)
    subjects = Subject.objects.filter(teacher=teacher)
    return render(request,'admins/teacher_profile.html',{'teacher':teacher,'subjects':subjects})
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
from standards.models import Standard
from accounts.models import User
from uploads.models import Upload
from students.forms import ProfilePicUpdateForm

@login_required
def student_home_view(request):
    user = request.user
    if not user.is_student:
        return HttpResponse('<h1>You are not authorised to view this page</h1>')
    student = Student.objects.get(user=user)
    subjects = Subject.objects.filter(standard=student.current_standard)
    uploads = {}
    for subject in subjects:
        uploads[subject] = Upload.objects.filter(subject=subject)
    context = {
        'subjects':subjects,
        'uploads':uploads,
    }
    return render(request,'students/home.html',context)

@login_required
def student_gradebook_view(request):
    user = request.user
    if not user.is_student:
        return HttpResponse('<h1>You are not authorised to view this page</h1>')
    student = Student.objects.get(user=user)
    examinations = Examination.objects.filter(standard=student.current_standard)
    results = {}
    for examination in examinations:
        results[examination] = Result.objects.filter(student=student,examination=examination).order_by('subject')
    subjects = Subject.objects.filter(standard=student.current_standard)
    standards = student.standards.all()
    dict = {
        'student':student,
        'results':results,
        'examinations':examinations,
        'subjects':subjects,
        'standards':standards,
        'standard': student.current_standard
    }
    return render(request,'students/gradebook.html',dict)

@login_required
def student_grades(request,slug):
    user = request.user
    standard = Standard.objects.get(slug=slug)
    if not user.is_student:
        return HttpResponse('<h1>You are not authorised to view this page</h1>')
    student = Student.objects.get(user=user)
    examinations = Examination.objects.filter(standard=standard)
    results = {}
    for examination in examinations:
        results[examination] = Result.objects.filter(student=student,examination=examination).order_by('subject')
    subjects = Subject.objects.filter(standard=standard)
    dict = {
        'student':student,
        'standard':standard,
        'results':results,
        'examinations':examinations,
        'subjects':subjects
    }
    return render(request,'students/grades.html',dict)

@login_required
def student_profile_view(request,slug=None):
    user = request.user
    if slug is None:
        student = user.student
    else:
        student = Student.objects.get(slug=slug)
    return render(request,'students/profile.html',{'student':student})
    
@login_required
def profile_pic_update_view(request):
    user = request.user
    if not user.is_student:
        return HttpResponse('<h1>Invalid request</h1>')
    student = user.student
    if request.method == 'POST':
        form = ProfilePicUpdateForm(request.POST, request.FILES,instance=user)
        form.save()
        return redirect('students:profile',slug=student.slug)
    form = ProfilePicUpdateForm(instance=user)
    return render(request,'students/profile_pic_update.html',{'form':form })


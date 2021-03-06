from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView,ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.contrib.auth import authenticate, get_user_model, login
from django.core.files.storage import FileSystemStorage

from students.models import Student
from results.models import Result, Examination
from teachers.models import Teacher
from subjects.models import Subject
from standards.models import Standard, ClassTeacher
from accounts.models import User

from .forms import UploadFileForm
from students.forms import ProfilePicUpdateForm

class TeacherTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'teachers/home.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if not user.is_teacher:
            return HttpResponse('<h1>You are not a teacher</h1>')
        teacher = Teacher.objects.get(user=user)
        examinations = Examination.objects.all()
        context['name'] = teacher.user.get_full_name()
        try:
            subjects = Subject.objects.filter(teacher=teacher)
            context['subjects'] = subjects
        except Subject.DoesNotExist:
            pass
        try:
            class_teacher = ClassTeacher.objects.get(teacher=teacher)
            context['class_teacher'] = class_teacher
        except ClassTeacher.DoesNotExist:
            context['class_teacher'] = ""
        return context

@login_required
def teacher_profile_view(request,slug):
    teacher = Teacher.objects.get(slug=slug)
    subjects = Subject.objects.filter(teacher=teacher)
    return render(request,'teachers/profile.html',{'teacher':teacher,'subjects':subjects})

@login_required
def class_result_update(request,slug):
    subject = Subject.objects.get(slug=slug)
    if request.user != subject.teacher.user:
        return HttpResponse("<h1>You are not allowed to access the given details<h1>")
    students = Student.objects.filter(current_standard=subject.standard).order_by('roll_number')
    examinations = Examination.objects.filter(standard=subject.standard)

    if request.method == 'POST':
        for student in students:
            for examination in examinations:
                exam = examination.name
                result = Result.objects.get(student=student,subject=subject,examination=examination)
                x = str(student.roll_number) + " " + exam.name
                marks = request.POST.get(x)
                try:
                    result.marks_secured = int(marks)
                except:
                    result.marks_secured = None
                result.save()
        return redirect('teachers:home')

    results = {}
    for student in students:
        results[student] = {}
        for examination in examinations:
            try:
                result = Result.objects.get(student=student,subject=subject,examination=examination)
            except Result.DoesNotExist:
                result = Result(student=student,subject=subject,examination=examination)
                result.save()
            results[student][examination] = result

    my_dict = {
        'results':results,
        'subject':subject,
        'students':students,
        'examinations':examinations,
        'size':str(len(examinations))
    }

    return render(request,'teachers/update_result.html',context=my_dict)

@login_required
def upload_file(request):
    form = UploadFileForm(request.POST or None)
    if request.method == 'POST':
        upload_file = request.FILES('document')
        fs = FileSystemStorage()
        fs.save(upload_file.name, upload_file)
    return render(request,'teachers/upload.html',{'form':form})

@login_required
def class_teacher_home(request):
    if not request.user.teacher.class_teacher:
        return HttpResponse("<h1>You are not allowed to access the given details<h1>")
    teacher = request.user.teacher
    students = Student.objects.filter(current_standard=teacher.class_teacher.standard)
    return render(request,'standards/class_teacher_home.html',{'students':students})

@login_required
def student_grade_view(request,slug):
    student = Student.objects.get(slug=slug)
    standard = student.current_standard
    examinations = Examination.objects.filter(standard=standard)
    results = {}
    for examination in examinations:
        results[examination] = Result.objects.filter(student=student,examination=examination).order_by('subject')
    subjects = Subject.objects.filter(standard=standard)
    for result in results[examinations[0]]:
        subjects.append(result.subject)
    dict = {
        'student':student,
        'standard':standard,
        'results':results,
        'examinations':examinations,
        'subjects':subjects
    }
    return render(request,'students/grades.html',dict)

@login_required
def profile_pic_update_view(request):
    user = request.user
    if not user.is_teacher:
        return HttpResponse('<h1>Invalid request</h1>')
    teacher = user.teacher
    if request.method == 'POST':
        form = ProfilePicUpdateForm(request.POST, request.FILES,instance=user)
        form.save()
        return redirect('teachers:profile',slug=teacher.slug)
    form = ProfilePicUpdateForm(instance=user)
    return render(request,'teachers/profile_pic_update.html',{'form':form })

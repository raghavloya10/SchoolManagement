from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .forms import UploadForm
from .models import Upload
from subjects.models import Subject

@login_required
def upload_view(request,pk):
    if not request.user.is_teacher:
        return HttpResponse('<h1>You are not authorised to view this page</h1>')
    subject = Subject.objects.get(pk=pk)
    teacher = subject.teacher
    if teacher.user != request.user:
        return HttpResponse('<h1>You are not authorised to view this page</h1>')
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.subject = Subject.objects.get(pk=pk)
            upload.save()
            return redirect('teachers:upload',pk=pk)
        else:
            print(form.errors)

    else:
        form = UploadForm()
    pdfs = Upload.objects.filter(subject=subject)
    return render(request,'teachers/upload.html',{'form':form,'pdfs':pdfs})

@login_required
def delete_view(request,pk):
    pdf = Upload.objects.get(pk=pk)
    subject = pdf.subject
    teacher = subject.teacher
    if teacher.user != request.user:
        return HttpResponse('<h1>You are not authorised to view this page</h1>')
    pdf.delete()
    return redirect('teachers:upload',subject.pk)

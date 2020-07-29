from django import forms
from accounts.models import User
from standards.models import Standard
from students.models import Student
from teachers.models import Teacher
from standards.models import ClassTeacher
from django.contrib.auth import authenticate,logout,login

class ProfilePicUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('profile_pic',)

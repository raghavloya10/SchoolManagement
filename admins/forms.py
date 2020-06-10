from django import forms
from accounts.models import User
from standards.models import Standard
from students.models import Student
from teachers.models import Teacher
from django.contrib.auth import authenticate,logout,login

class UserSignupForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Retype Password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                'email', 'password1', 'password2',
                'date_of_birth','contact_no','address','profile_pic')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Password didn\'t match!')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class StudentExtraForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('admission_no','father','current_standard','roll_number','caste','religion')
        labels = {
            'father':"Father's name",
            'current_standard':"Standard",
        }

    def save(self, user, commit=True):
        student = super(StudentExtraForm, self).save(commit=False)
        student.user = user
        if commit:
            student.save()
        return student

class StudentUpdateForm(forms.ModelForm):

    class Meta:
        model = Student
        exclude = ('user',)

class RefreshStandardForm(forms.Form):
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all().order_by('current_standard'),
                                              widget=forms.CheckboxSelectMultiple,
                                              label='Select all the students to be enrolled in the standard:')

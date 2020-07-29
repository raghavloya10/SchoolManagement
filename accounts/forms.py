from django import forms
from accounts.models import User
from standards.models import Standard
from students.models import Student
from teachers.models import Teacher
from django.contrib.auth import authenticate,logout,login

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'student@example.com',
                                                            'class':'input-box'}),label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password',
                                                                 'class':'input-box'}),label='')

    # class Meta():
    #     widgets = {
    #         'email': forms.EmailInput(attrs={'class':'textinputclass', 'placeholder':'student@example.com'}),
    #         'password': forms.TextInput(attrs={'class':''})
    #     }

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")

        return super(UserLoginForm, self).clean(*args, **kwargs)

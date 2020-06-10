from django.core.exceptions import ValidationError
from django import forms
import os

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    print(ext)
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise forms.ValidationError('Please convert the file into pdf and then try uploading!')

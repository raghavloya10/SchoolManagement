from django.contrib import admin
from .models import Examination, Result, ExaminationName
# Register your models here.

admin.site.register(ExaminationName)
admin.site.register(Examination)
admin.site.register(Result)

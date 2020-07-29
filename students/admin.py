from django.contrib import admin
from .models import Student
# Register your models here.

# class ResultAdmin(admin.ModelAdmin):
#     fields = ['student','subject','marks_secured']
#     search_fields = ['marks_secured']
#     list_filter = ['student']
#     list_display = ['student','subject','marks_secured']
#     list_editable = ['marks_secured']

admin.site.register(Student)
# admin.site.register(Result,ResultAdmin)

#python manage.py dbshell
#.tab
#.schema tab
#.schema <app_name>
#update 0001_initial.py in migrations.py
#alter table "<table_name>" add column

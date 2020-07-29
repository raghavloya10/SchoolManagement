from django.db import models
from django.urls import reverse
from subjects.models import Subject
from students.models import Student
from standards.models import Standard
from django.db.models.signals import pre_save
from django.utils.text import slugify
# Create your models here.

class ExaminationName(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Examination(models.Model):
    name = models.ForeignKey(ExaminationName,on_delete=models.CASCADE)
    standard = models.ForeignKey(Standard,on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.name,self.standard)

class Result(models.Model):
    marks_secured = models.PositiveIntegerField(blank=True,null=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,blank=True,null=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE,blank=True,null=True)
    examination = models.ForeignKey(Examination,on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        ordering = []

    def __str__(self):
        return "{} - Roll {} - {}".format(self.student.current_standard, self.student.roll_number,self.subject.name)

from django.db import models
from django.db.models.signals import post_save, pre_save
from teachers.models import Teacher
from accounts.utils import unique_name_slug_generator

class Standard(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=205, null=True, blank=True, editable=False)

    def __str__(self):
        return self.name

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_name_slug_generator(instance)

pre_save.connect(slug_generator,sender=Standard)

class ClassTeacher(models.Model):
    standard = models.ForeignKey(Standard,on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.standard, self.teacher)

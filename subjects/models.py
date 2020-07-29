from django.db import models
from django.db.models.signals import post_save, pre_save

from teachers.models import Teacher
from standards.models import Standard

from accounts.utils import unique_name_slug_generator

class SubjectName(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.ForeignKey(SubjectName, on_delete=models.CASCADE)
    standard = models.ForeignKey(Standard,on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    total_marks = models.PositiveIntegerField(default=100,null=True,blank=True)
    classes_per_week = models.PositiveIntegerField(default=6,null=True,blank=True)
    slug = models.SlugField(max_length=210,null=True,blank=True,editable=False)

    def get_subject_name(self):
        return self.name.name

    def __str__(self):
        return self.name.name

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_name_slug_generator(instance)

pre_save.connect(slug_generator,sender=Subject)

#

# from django.db.models.signals import post_save
# from django.dispatch import receiver

# @receiver(post_save, sender=auth_User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Teacher.objects.create(user=instance)
#
# @receiver(post_save, sender=auth_User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

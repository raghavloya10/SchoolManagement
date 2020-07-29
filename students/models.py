from django.db import models
from django.urls import reverse
from django.utils import timezone

from standards.models import Standard
from accounts.models import User

from django.db.models.signals import pre_save
from accounts.utils import unique_email_slug_generator
# Create your models here.

CASTE_CHOICES = (
    ("BC", "BC"),
    ("OBC", "OBC"),
    ("SC", "SC"),
    ("ST", "ST"),
    ("General", "General"),
    ("Other", "Other"),
)

RELIGION_CHOICES = (
    ("Hindu", "Hindu"),
    ("Muslim", "Muslim"),
    ("Christian", "Christian"),
    ("Other", "Other"),
)

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    standards = models.ManyToManyField(Standard)
    current_standard = models.ForeignKey(Standard,related_name='Class',on_delete=models.CASCADE,null=True,blank=True)
    roll_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at = models.DateTimeField(auto_now=True,editable=False)
    admission_no = models.CharField(max_length=20)
    father = models.CharField(max_length=200)
    slug = models.SlugField(max_length=210,blank=True,null=True,editable=False)
    caste = models.CharField(max_length=20,
                             choices=CASTE_CHOICES,
                             default="General")
    religion = models.CharField(max_length=10,
                                choices=RELIGION_CHOICES,
                                default='Hindu')

    def __str__(self):
        return str(self.user)


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_email_slug_generator(instance)

pre_save.connect(slug_generator,sender=Student)

    # class Meta:
    #     ordering = []
